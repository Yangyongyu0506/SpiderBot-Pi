// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from hardware_interface:msg/BuzzerDuty.idl
// generated code does not contain a copyright notice

#ifndef HARDWARE_INTERFACE__MSG__DETAIL__BUZZER_DUTY__STRUCT_H_
#define HARDWARE_INTERFACE__MSG__DETAIL__BUZZER_DUTY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/BuzzerDuty in the package hardware_interface.
typedef struct hardware_interface__msg__BuzzerDuty
{
  /// 0-255
  uint8_t duty_cycle;
} hardware_interface__msg__BuzzerDuty;

// Struct for a sequence of hardware_interface__msg__BuzzerDuty.
typedef struct hardware_interface__msg__BuzzerDuty__Sequence
{
  hardware_interface__msg__BuzzerDuty * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} hardware_interface__msg__BuzzerDuty__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // HARDWARE_INTERFACE__MSG__DETAIL__BUZZER_DUTY__STRUCT_H_
