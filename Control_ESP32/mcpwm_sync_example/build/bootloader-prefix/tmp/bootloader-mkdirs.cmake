# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "C:/Users/mathrisk/esp/esp-idf/components/bootloader/subproject"
  "C:/Users/mathrisk/Desktop/REPOS/DABREPO/Control_ESP32/mcpwm_sync_example/build/bootloader"
  "C:/Users/mathrisk/Desktop/REPOS/DABREPO/Control_ESP32/mcpwm_sync_example/build/bootloader-prefix"
  "C:/Users/mathrisk/Desktop/REPOS/DABREPO/Control_ESP32/mcpwm_sync_example/build/bootloader-prefix/tmp"
  "C:/Users/mathrisk/Desktop/REPOS/DABREPO/Control_ESP32/mcpwm_sync_example/build/bootloader-prefix/src/bootloader-stamp"
  "C:/Users/mathrisk/Desktop/REPOS/DABREPO/Control_ESP32/mcpwm_sync_example/build/bootloader-prefix/src"
  "C:/Users/mathrisk/Desktop/REPOS/DABREPO/Control_ESP32/mcpwm_sync_example/build/bootloader-prefix/src/bootloader-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "C:/Users/mathrisk/Desktop/REPOS/DABREPO/Control_ESP32/mcpwm_sync_example/build/bootloader-prefix/src/bootloader-stamp/${subDir}")
endforeach()
