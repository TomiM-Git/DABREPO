//### CODIGO DE PROGRAMACIÓN DE MICROCONTROLADOR PARA ###
//### CONTROL DE FLUJO DE POTENCIA DE CONVERTIDOR DAB ###

// Autor: Magnelli, Tomás Vicente.
// Contexto: PROYECTO INTEGRADOR PARA LA OBTENCIÓN DEL TÍTULO DE GRADO
// INGENIERO ELECTRÓNICO
// Titulo del proyecto: “CONTROL DE POTENCIA DE UN CONVERTIDOR AISLADO 
// MODULAR DE TOPOLOGÍA DOBLE PUENTE ACTIVO”.
//  
// Director de Proyecto Integrador: Esp. Ing. Adrián Claudio Agüero
// Universidad Nacional de Cordoba.
// Facultad de Ciencias Exactas, Físicas y Naturales.
// Programa de autoría parcialmente propia, algunas partes recopiladas
// de los ejemplos de utilizacion de periféricos que provee el creador
// y diseñador del microcontrolador, Espressif Systems. 
// El programa fue realizado para uso específico para del 
// Proyecto Integrador mencionado pero es de uso libre.
//  
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

// ************ Parametros principales a modificar para control PWM. ************
// Frecuencia de señal PWM proveniente de ESP32.
#define FREC 25000   
// Desfase entre 0 y 1000 (Desde 0: sin desfase. Hasta 1000: Un periodo completo).
#define SHIFT 200 
// Tiempo muerto entre disparos en una misma pierna de puente H.   
#define DTIME 10 // Ejemplo: si DTIME=10 => td=DTIME*100ns=10*100ns=1us.

// Definiciones generales
const static char *TAG = "CONSOL MSG:";
// Definiciones PWM
#define TARGET_MCPWM_UNIT MCPWM_UNIT_0  // Periferico MCPWM a utilizado.
#define MCPWM0A_OUTPUT_GPIO GPIO_NUM_13 // GPIO13 para control Gate 1 y Gate 4.
#define MCPWM0B_OUTPUT_GPIO GPIO_NUM_12 // GPIO12 para control Gate 2 y Gate 3.
#define MCPWM1A_OUTPUT_GPIO GPIO_NUM_14 // GPIO14 para control Gate 5 y Gate 8.
#define MCPWM1B_OUTPUT_GPIO GPIO_NUM_27 // GPIO27 para control Gate 6 y Gate 7.
#define SIMU_GPIO_SYNC_SOURCE_GPIO GPIO_NUM_21 // GPIO21 salida de sincronismo.
#define SIMU_GPIO_SYNC_SIMULATE_GPIO GPIO_NUM_19 // GPIO19 entrada de sincronismo.
// Definiciones ADC y UART
#define DEFAULT_VREF    1100
#define TXD_PIN (GPIO_NUM_17)
#define RXD_PIN (GPIO_NUM_16)
static esp_adc_cal_characteristics_t *adc_chars;
static const adc_channel_t CHN6 = ADC_CHANNEL_6;     //GPIO34
static const adc_channel_t CHN7 = ADC_CHANNEL_7;     //GPIO35
static const adc_bits_width_t width = ADC_WIDTH_BIT_12;
static const adc_atten_t atten = ADC_ATTEN_DB_11;
static const int RX_BUF_SIZE = 1024;
//Inicialización de funciones.
esp_err_t conf_PWM(void);
esp_err_t sync_PWM(void);
esp_err_t gpio_bind_PWM(void);
esp_err_t conf_ADC(void);
esp_err_t conf_UART(void);
void sendData(const char* data);
// Bloque de código principal.
void app_main(void){    
    conf_UART();    //Configura periférico UART.
    conf_ADC();     //Configura periférico ADC.
    conf_PWM();     //Configura periférico MCPWM.
    ESP_LOGI(TAG, "FIN DE CONFIGURACION.");//Imprime mensaje en pantalla.
    sync_PWM();     //Sincronización de señales PWM para desfase asignado.
    ESP_LOGI(TAG, "SEÑALES SINCRONIZADAS.");//Imprime mensaje en pantalla.
    //Asocia pines de GPIO para habilitar salidas PWM ya sincronizadas.
    gpio_bind_PWM();
    ESP_LOGI(TAG, "SALIDAS PWM HABILITADAS.");
    char str_send[19]; //Defino variable para enviar datos de lecturas de adc.
    while (1) {
        int32_t adc_reading_6 = 0;//Defino variable para lectura de ADC en CHN6.
        int32_t adc_reading_7 = 0;//Defino variable para lectura de ADC en CHN7.
        adc_reading_6 += adc1_get_raw((adc1_channel_t)CHN6);//Almaceno lectura.
        adc_reading_7 += adc1_get_raw((adc1_channel_t)CHN7);//Almaceno lectura.
        //Obtengo valores de corriente en funcion de lectura.
        int32_t current_IN  = (adc_reading_6-2048)*50/2048;
        int32_t current_OUT = (adc_reading_7-2048)*50/2048;
        //Líneas para debuggeo imprimiendo mediciones en consola.
//        printf("CHN6:\tRaw: %d\tVoltage: %d [mV]\tCurrent_IN_DAB:
//%d [A]\n", adc_reading_6, voltage_6,current_IN); //(Sacar salto de línea)
//        printf("CHN7:\tRaw: %d\tVoltage: %d [mV]\tCurrent_OUT_DAB:
// %d [A]\n", adc_reading_7, voltage_7,current_OUT);//(Sacar salto de línea)
        //Preparo un string en formato "-25" para enviar -25A.
        sprintf(str_send,"%d,%d\r",current_IN,current_OUT);  
//Envío string con formato "-25" al osciloscopio digital 
        uart_write_bytes(UART_NUM_2,str_send,8);
        vTaskDelay(pdMS_TO_TICKS(10));
        //Variar tiempo de retardo segun frecuencia de muestreo deseada.
        // Es importante tener en cuenta que las funciones 
        // sprintf() y uart_write_bytes() requieren mucho tiempo de ejecución
        //  y esto tambien limita la frecuencia de muestreo del ADC.
    }
}
// Funciones especificas UART
esp_err_t conf_UART(void){//Configura periférico UART.
    const uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_APB,
    };
    uart_driver_install(UART_NUM_2, RX_BUF_SIZE * 2, 0, 0, NULL, 0);
    uart_param_config(UART_NUM_2, &uart_config);
    uart_set_pin(UART_NUM_2,TXD_PIN,RXD_PIN,UART_PIN_NO_CHANGE,UART_PIN_NO_CHANGE);
    return ESP_OK;
}
// Funciones especificas ADC
esp_err_t conf_ADC(void){//Configura periférico ADC.
    ESP_ERROR_CHECK(adc1_config_width(width));
    ESP_ERROR_CHECK(adc1_config_channel_atten(CHN6, atten));
    ESP_ERROR_CHECK(adc1_config_channel_atten(CHN7, atten));
    adc_chars = calloc(1, sizeof(esp_adc_cal_characteristics_t));
    return ESP_OK;
}
// Funciones especificas PWM
esp_err_t conf_PWM(void){   //Configura periférico PWM.
    ESP_LOGI(TAG, "INICIO CONFIGURACION...");
    vTaskDelay(pdMS_TO_TICKS(500));
    // Inicializo estructura con frecuencia parametrizada,
    // 50% de ciclo util en ambos canales, con contador ascendente.
    mcpwm_config_t pwm_config = {
        .frequency = FREC,    // PARÁMETRO FREC PARAMETRIZADO EN SECTOR #DEFINE
        .cmpr_a = 50,
        .cmpr_b = 50,
        .counter_mode = MCPWM_UP_COUNTER,
        .duty_mode = MCPWM_DUTY_MODE_0,
    };
    ESP_ERROR_CHECK(mcpwm_init(TARGET_MCPWM_UNIT, MCPWM_TIMER_0, &pwm_config));
    ESP_ERROR_CHECK(mcpwm_init(TARGET_MCPWM_UNIT, MCPWM_TIMER_1, &pwm_config));
    vTaskDelay(pdMS_TO_TICKS(1000));
    //  PARÁMETRO DTIME DE LAS SIGUIENTES DOS LÍNEAS PARAMETRIZADO EN SECTOR #DEFINE 
    ESP_ERROR_CHECK(mcpwm_deadtime_enable(TARGET_MCPWM_UNIT,MCPWM_TIMER_0,MCPWM_ACTIVE_HIGH_COMPLIMENT_MODE,DTIME,DTIME));
    ESP_ERROR_CHECK(mcpwm_deadtime_enable(TARGET_MCPWM_UNIT,MCPWM_TIMER_1,MCPWM_ACTIVE_HIGH_COMPLIMENT_MODE,DTIME,DTIME));
    vTaskDelay(pdMS_TO_TICKS(1000));
    return ESP_OK;
}
esp_err_t sync_PWM(void){
    ESP_LOGI(TAG,"SINCRONIZANDO SEÑALES PWM...");
    mcpwm_sync_config_t sync_PUENTE_ENTRADA = {
        .sync_sig = MCPWM_SELECT_GPIO_SYNC0,
        .timer_val = 0,   // Valor nulo de desplazamiento al puente P1.
        .count_direction = MCPWM_TIMER_DIRECTION_UP,
    };
    mcpwm_sync_config_t sync_PUENTE_SALIDA = {
        .sync_sig = MCPWM_SELECT_GPIO_SYNC0,
        .timer_val = SHIFT, // PARÁMETRO SHIFT PARAMETRIZADO EN SECTOR #DEFINE.
        .count_direction = MCPWM_TIMER_DIRECTION_UP,
    };// A continuación se asigna cada estructura al timer
    //  correspondiente al sincronismo deseado en cada puente.
    ESP_ERROR_CHECK(mcpwm_sync_configure(TARGET_MCPWM_UNIT, MCPWM_TIMER_0, &sync_PUENTE_SALIDA));
    ESP_ERROR_CHECK(mcpwm_sync_configure(TARGET_MCPWM_UNIT, MCPWM_TIMER_1, &sync_PUENTE_ENTRADA));
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
    vTaskDelay(pdMS_TO_TICKS(100));//Demora necesaria para garantizar sincronismo, no reducir.
    return ESP_OK;
}
esp_err_t gpio_bind_PWM(void){//Habilita las salidas MCPWMxx.
    ESP_LOGI(TAG, "HABILITANDO SALIDAS PWM...");
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM0A, MCPWM0A_OUTPUT_GPIO));
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM0B, MCPWM0B_OUTPUT_GPIO));
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM1A, MCPWM1A_OUTPUT_GPIO));
    ESP_ERROR_CHECK(mcpwm_gpio_init(TARGET_MCPWM_UNIT, MCPWM1B, MCPWM1B_OUTPUT_GPIO));
    return ESP_OK;
}