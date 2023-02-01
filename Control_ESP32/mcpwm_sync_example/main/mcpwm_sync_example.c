//Librerias generales
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "driver/gpio.h"
//Librerias PWM
#include "freertos/queue.h"
#include "esp_rom_gpio.h"
#include "soc/mcpwm_periph.h"
#include "hal/gpio_hal.h"
#include "esp_check.h"
#include "soc/rtc.h"
#include "driver/mcpwm.h"
// Librerias ADC
#include <stdio.h>
#include <stdlib.h>
#include "driver/adc.h"
#include "esp_adc_cal.h"
// Librerias UART
#include "esp_system.h"
#include "driver/uart.h"
#include "string.h"

// Definiciones generales

const static char *TAG = "CONSOL MSG:";

// Definiciones PWM
#define TARGET_MCPWM_UNIT MCPWM_UNIT_0  // Periferico MCPWM a utilizado
#define MCPWM0A_OUTPUT_GPIO GPIO_NUM_13 // GPIO13 para control Gate 1 y Gate 4
#define MCPWM0B_OUTPUT_GPIO GPIO_NUM_12 // GPIO12 para control Gate 2 y Gate 3
#define MCPWM1A_OUTPUT_GPIO GPIO_NUM_14 // GPIO14 para control Gate 5 y Gate 8
#define MCPWM1B_OUTPUT_GPIO GPIO_NUM_27 // GPIO27 para control Gate 6 y Gate 7
#define SIMU_GPIO_SYNC_SOURCE_GPIO GPIO_NUM_21 // GPIO21 para fuente de sincronismo de desfase entre puentes
#define SIMU_GPIO_SYNC_SIMULATE_GPIO GPIO_NUM_19 // GPIO19 para recepcion de señal de sincronismo

#define FREC 1000   // Frecuencia de señal PWM proveniente de ESP32.
#define DESFASE 300    // Desfase entre 0 y 1000 (Desde 0: sin desfase. Hasta 1000: Un periodo completo)
#define DTIME 4000  // Tiempo muerto entre disparos en una misma pierna de puente H. Ecuacion abajo.
// td = DTIME*100ns (Ejemplo: si DTIME=4000 => td=DTIME*100ns=4000*100ns=400us)

esp_err_t conf_PWM(void);
esp_err_t sync_PWM(void);
esp_err_t gpio_bind_PWM(void);

// Definiciones ADC
#define DEFAULT_VREF    1100        //Use adc2_vref_to_gpio() to obtain a better estimate
#define NO_OF_SAMPLES   8          //Multisampling

static esp_adc_cal_characteristics_t *adc_chars;
static const adc_channel_t CHN6 = ADC_CHANNEL_6;     //GPIO34
static const adc_channel_t CHN7 = ADC_CHANNEL_7;     //GPIO35
static const adc_bits_width_t width = ADC_WIDTH_BIT_12;
static const adc_atten_t atten = ADC_ATTEN_DB_11;

esp_err_t conf_ADC(void);

// Definiciones UART

static const int RX_BUF_SIZE = 1024;

#define TXD_PIN (GPIO_NUM_17)
#define RXD_PIN (GPIO_NUM_16)

//char str_send[];

esp_err_t conf_UART(void);
void sendData(const char* data);

// Codigo principal

void app_main(void){
    conf_UART();
    conf_ADC();
    conf_PWM();
    ESP_LOGI(TAG, "FIN DE CONFIGURACION.");
    sync_PWM();
    ESP_LOGI(TAG, "SEÑALES SINCRONIZADAS.");
    gpio_bind_PWM();
    ESP_LOGI(TAG, "SALIDAS PWM HABILITADAS.");

    char str_send[19];
    while (1) {
        int32_t adc_reading_6 = 0;
        int32_t adc_reading_7 = 0;
        //Multisampling
        /*
        for (int i = 0; i < NO_OF_SAMPLES; i++) {
            adc_reading_6 += adc1_get_raw((adc1_channel_t)CHN6);
            adc_reading_7 += adc1_get_raw((adc1_channel_t)CHN7);
        }*/
        adc_reading_6 += adc1_get_raw((adc1_channel_t)CHN6);
        adc_reading_7 += adc1_get_raw((adc1_channel_t)CHN7);

//        adc_reading_6 /= NO_OF_SAMPLES;
//        adc_reading_7 /= NO_OF_SAMPLES;
        //Convert adc_reading to voltage in mV
//        uint32_t voltage_6 = esp_adc_cal_raw_to_voltage(adc_reading_6, adc_chars);
//        uint32_t voltage_7 = esp_adc_cal_raw_to_voltage(adc_reading_7, adc_chars);

        int32_t current_IN  = (adc_reading_6-2048)*50/2048;
        int32_t current_OUT = (adc_reading_7-2048)*50/2048;

//        printf("CHN6:\tRaw: %d\tVoltage: %d [mV]\tCurrent_IN_DAB:  %d [A]\n", adc_reading_6, voltage_6,current_IN);
//        printf("CHN7:\tRaw: %d\tVoltage: %d [mV]\tCurrent_OUT_DAB: %d [A]\n", adc_reading_7, voltage_7,current_OUT);

        sprintf(str_send,"%d,%d\r",current_IN,current_OUT);  //"-25"
//        const int len = strlen(str_send);
//        printf("strlen(data)=%d",len);
        uart_write_bytes(UART_NUM_2,str_send,8);
//        sendData(str_send);
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}
// Funciones especificas UART
esp_err_t conf_UART(void){
    const uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_APB,
    };
    // We won't use a buffer for sending data.
    uart_driver_install(UART_NUM_2, RX_BUF_SIZE * 2, 0, 0, NULL, 0);
    uart_param_config(UART_NUM_2, &uart_config);
    uart_set_pin(UART_NUM_2, TXD_PIN, RXD_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    return ESP_OK;
}

void sendData(const char* data){
    const int len = strlen(data);
//    const int txBytes = 
    uart_write_bytes(UART_NUM_2, data, len);
    return;
}
// Funciones especificas ADC
esp_err_t conf_ADC(void){
    ESP_ERROR_CHECK(adc1_config_width(width));
    ESP_ERROR_CHECK(adc1_config_channel_atten(CHN6, atten));
    ESP_ERROR_CHECK(adc1_config_channel_atten(CHN7, atten));
    adc_chars = calloc(1, sizeof(esp_adc_cal_characteristics_t));
    return ESP_OK;
}
// Funciones especificas PWM
esp_err_t conf_PWM(void){   
    ESP_LOGI(TAG, "INICIO CONFIGURACION...");
    vTaskDelay(pdMS_TO_TICKS(500));
    // Inicializo estructura con frecuencia parametrizada, 50% de ciclo util en ambos canales, con contador ascendente.
    mcpwm_config_t pwm_config = {
        .frequency = FREC,    // PARAMETRO FREC PARAMETRIZADO EN SECTOR #DEFINE
        .cmpr_a = 50,
        .cmpr_b = 50,
        .counter_mode = MCPWM_UP_COUNTER,
        .duty_mode = MCPWM_DUTY_MODE_0,
    };
    ESP_ERROR_CHECK(mcpwm_init(TARGET_MCPWM_UNIT, MCPWM_TIMER_0, &pwm_config));
    ESP_ERROR_CHECK(mcpwm_init(TARGET_MCPWM_UNIT, MCPWM_TIMER_1, &pwm_config));
    vTaskDelay(pdMS_TO_TICKS(1000));
    // PARAMETRO DTIME PARAMETRIZADO EN SECTOR #DEFINE
    ESP_ERROR_CHECK(mcpwm_deadtime_enable(TARGET_MCPWM_UNIT,MCPWM_TIMER_0,MCPWM_ACTIVE_HIGH_COMPLIMENT_MODE,DTIME,DTIME));
    ESP_ERROR_CHECK(mcpwm_deadtime_enable(TARGET_MCPWM_UNIT,MCPWM_TIMER_1,MCPWM_ACTIVE_HIGH_COMPLIMENT_MODE,DTIME,DTIME));
    vTaskDelay(pdMS_TO_TICKS(1000));
    return ESP_OK;
}
esp_err_t sync_PWM(void){
    ESP_LOGI(TAG,"SINCRONIZANDO SEÑALES PWM...");
    mcpwm_sync_config_t sync_PUENTE_ENTRADA = {
        .sync_sig = MCPWM_SELECT_GPIO_SYNC0,
        .timer_val = 0,
        .count_direction = MCPWM_TIMER_DIRECTION_UP,
    };
    mcpwm_sync_config_t sync_PUENTE_SALIDA = {
        .sync_sig = MCPWM_SELECT_GPIO_SYNC0,
        .timer_val = DESFASE,                              // PARAMETRO DESFASE PARAMETRIZADO EN SECTOR #DEFINE
        .count_direction = MCPWM_TIMER_DIRECTION_UP,
    };
    ESP_ERROR_CHECK(mcpwm_sync_configure(TARGET_MCPWM_UNIT, MCPWM_TIMER_0, &sync_PUENTE_ENTRADA));
    ESP_ERROR_CHECK(mcpwm_sync_configure(TARGET_MCPWM_UNIT, MCPWM_TIMER_1, &sync_PUENTE_SALIDA));
    // then configure GPIO
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM_SYNC_0, SIMU_GPIO_SYNC_SOURCE_GPIO));

    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_OUTPUT;
    io_conf.pin_bit_mask = BIT64(SIMU_GPIO_SYNC_SIMULATE_GPIO);
    io_conf.pull_down_en = 0;
    io_conf.pull_up_en = 0;

    ESP_ERROR_CHECK(gpio_config(&io_conf));
    ESP_ERROR_CHECK(gpio_set_level(SIMU_GPIO_SYNC_SIMULATE_GPIO, 0));
    ESP_ERROR_CHECK(gpio_set_level(SIMU_GPIO_SYNC_SIMULATE_GPIO, 1));
    // wait for at least one TEP
    vTaskDelay(pdMS_TO_TICKS(10));
    // re-enable GPIO output, to see the result
//    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM0A, TIMER0_OUTPUT_GPIO));
//    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM1A, TIMER1_OUTPUT_GPIO));
//    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM2A, TIMER2_OUTPUT_GPIO));
//    ESP_LOGI(TAG, "Output should already be synchronized");
    vTaskDelay(pdMS_TO_TICKS(1000));
    return ESP_OK;
}
esp_err_t gpio_bind_PWM(void){
    ESP_LOGI(TAG, "HABILITANDO SALIDAS PWM...");
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM0A, MCPWM0A_OUTPUT_GPIO));
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM0B, MCPWM0B_OUTPUT_GPIO));
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM1A, MCPWM1A_OUTPUT_GPIO));
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM1B, MCPWM1B_OUTPUT_GPIO));
    return ESP_OK;
}

/*

    vTaskDelay(pdMS_TO_TICKS(1000));
    // temporarily disable GPIO output, by binding to GenBs which have 0 output
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM0B, TIMER0_OUTPUT_GPIO));
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM1B, TIMER1_OUTPUT_GPIO));
//    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM2B, TIMER2_OUTPUT_GPIO));
    vTaskDelay(pdMS_TO_TICKS(2000));


//////////////////////////////////////////////////////////////////
    // stop and restart timers to mess them
    ESP_ERROR_CHECK(mcpwm_stop(TARGET_MCPWM_UNIT, MCPWM_TIMER_2));
    ESP_ERROR_CHECK(mcpwm_stop(TARGET_MCPWM_UNIT, MCPWM_TIMER_1));
//    ESP_ERROR_CHECK(mcpwm_stop(TARGET_MCPWM_UNIT, MCPWM_TIMER_0));
    vTaskDelay(pdMS_TO_TICKS(2000));
    ESP_ERROR_CHECK(mcpwm_start(TARGET_MCPWM_UNIT, MCPWM_TIMER_0));
    ESP_ERROR_CHECK(mcpwm_start(TARGET_MCPWM_UNIT, MCPWM_TIMER_1));
//    ESP_ERROR_CHECK(mcpwm_start(TARGET_MCPWM_UNIT, MCPWM_TIMER_2));
    ESP_LOGI(TAG, "force synchronous lost");

    vTaskDelay(pdMS_TO_TICKS(1000));

    // temporarily disable GPIO output, by binding to GenBs which have 0 output
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM0B, TIMER0_OUTPUT_GPIO));
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM1B, TIMER1_OUTPUT_GPIO));
//    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM2B, TIMER2_OUTPUT_GPIO));
    vTaskDelay(pdMS_TO_TICKS(2000));

#ifdef SOC_MCPWM_SWSYNC_CAN_PROPAGATE
    // use the trick that only available on esp32s3
    mcpwm_set_timer_sync_output(MCPWM_UNIT_0, MCPWM_TIMER_0, MCPWM_SWSYNC_SOURCE_SYNCIN);
    sync_conf.sync_sig = MCPWM_SELECT_TIMER0_SYNC;
    mcpwm_sync_configure(MCPWM_UNIT_0, MCPWM_TIMER_0, &sync_conf);
    mcpwm_sync_configure(MCPWM_UNIT_0, MCPWM_TIMER_1, &sync_conf);
    mcpwm_sync_configure(MCPWM_UNIT_0, MCPWM_TIMER_2, &sync_conf);
    // then send soft sync event to timer0
    mcpwm_timer_trigger_soft_sync(MCPWM_UNIT_0, MCPWM_TIMER_0);
    // re-enable GPIO output
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM0A, TIMER0_OUTPUT_GPIO));
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM1A, TIMER1_OUTPUT_GPIO));
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM2A, TIMER2_OUTPUT_GPIO));
    ESP_LOGI(TAG, "Output should already be synchronized on esp32s3");

    vTaskDelay(pdMS_TO_TICKS(1000));
#endif
////////////////////////////////////////////////////////////////////
    // temporarily disable GPIO output, by binding to GenBs which have 0 output
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM0B, TIMER0_OUTPUT_GPIO));
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM1B, TIMER1_OUTPUT_GPIO));
//    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM2B, TIMER2_OUTPUT_GPIO));
    vTaskDelay(pdMS_TO_TICKS(2000));
    // create phase between each timer.
    // for this case all timers has 10% of period phase between each other
    sync_conf.sync_sig = MCPWM_SELECT_GPIO_SYNC0;
    sync_conf.timer_val = 0;  // no phase applied
    mcpwm_sync_configure(MCPWM_UNIT_0, MCPWM_TIMER_0, &sync_conf);
//    sync_conf.timer_val = 900;  // fill the counter with 90.0% of period will cause next pulse being delayed 10% period
//    mcpwm_sync_configure(MCPWM_UNIT_0, MCPWM_TIMER_1, &sync_conf);
    sync_conf.timer_val = 800;  // fill the counter with 80.0% of period will cause next pulse being delayed 20% period
    mcpwm_sync_configure(MCPWM_UNIT_0, MCPWM_TIMER_1, &sync_conf);
    // trigger positive edge
    ESP_ERROR_CHECK(gpio_set_level(SIMU_GPIO_SYNC_SIMULATE_GPIO, 0));
    ESP_ERROR_CHECK(gpio_set_level(SIMU_GPIO_SYNC_SIMULATE_GPIO, 1));
    // wait for at least one TEP
    vTaskDelay(pdMS_TO_TICKS(10));
    // re-enable GPIO output, to see the result
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM0A, TIMER0_OUTPUT_GPIO));
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM1A, TIMER1_OUTPUT_GPIO));
//    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM2A, TIMER2_OUTPUT_GPIO));
    ESP_LOGI(TAG, "Each output pulse should be placed with 10 percents of period");

    vTaskDelay(pdMS_TO_TICKS(1000));

    */

//    ESP_ERROR_CHECK(mcpwm_stop(TARGET_MCPWM_UNIT, MCPWM_TIMER_2));
//    ESP_ERROR_CHECK(mcpwm_stop(TARGET_MCPWM_UNIT, MCPWM_TIMER_1));
//    ESP_ERROR_CHECK(mcpwm_stop(TARGET_MCPWM_UNIT, MCPWM_TIMER_0));
