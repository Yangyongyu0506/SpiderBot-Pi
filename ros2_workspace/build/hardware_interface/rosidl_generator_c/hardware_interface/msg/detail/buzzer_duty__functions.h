// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from hardware_interface:msg/BuzzerDuty.idl
// generated code does not contain a copyright notice

#ifndef HARDWARE_INTERFACE__MSG__DETAIL__BUZZER_DUTY__FUNCTIONS_H_
#define HARDWARE_INTERFACE__MSG__DETAIL__BUZZER_DUTY__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "hardware_interface/msg/rosidl_generator_c__visibility_control.h"

#include "hardware_interface/msg/detail/buzzer_duty__struct.h"

/// Initialize msg/BuzzerDuty message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * hardware_interface__msg__BuzzerDuty
 * )) before or use
 * hardware_interface__msg__BuzzerDuty__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_hardware_interface
bool
hardware_interface__msg__BuzzerDuty__init(hardware_interface__msg__BuzzerDuty * msg);

/// Finalize msg/BuzzerDuty message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_hardware_interface
void
hardware_interface__msg__BuzzerDuty__fini(hardware_interface__msg__BuzzerDuty * msg);

/// Create msg/BuzzerDuty message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * hardware_interface__msg__BuzzerDuty__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_hardware_interface
hardware_interface__msg__BuzzerDuty *
hardware_interface__msg__BuzzerDuty__create();

/// Destroy msg/BuzzerDuty message.
/**
 * It calls
 * hardware_interface__msg__BuzzerDuty__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_hardware_interface
void
hardware_interface__msg__BuzzerDuty__destroy(hardware_interface__msg__BuzzerDuty * msg);

/// Check for msg/BuzzerDuty message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_hardware_interface
bool
hardware_interface__msg__BuzzerDuty__are_equal(const hardware_interface__msg__BuzzerDuty * lhs, const hardware_interface__msg__BuzzerDuty * rhs);

/// Copy a msg/BuzzerDuty message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_hardware_interface
bool
hardware_interface__msg__BuzzerDuty__copy(
  const hardware_interface__msg__BuzzerDuty * input,
  hardware_interface__msg__BuzzerDuty * output);

/// Initialize array of msg/BuzzerDuty messages.
/**
 * It allocates the memory for the number of elements and calls
 * hardware_interface__msg__BuzzerDuty__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_hardware_interface
bool
hardware_interface__msg__BuzzerDuty__Sequence__init(hardware_interface__msg__BuzzerDuty__Sequence * array, size_t size);

/// Finalize array of msg/BuzzerDuty messages.
/**
 * It calls
 * hardware_interface__msg__BuzzerDuty__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_hardware_interface
void
hardware_interface__msg__BuzzerDuty__Sequence__fini(hardware_interface__msg__BuzzerDuty__Sequence * array);

/// Create array of msg/BuzzerDuty messages.
/**
 * It allocates the memory for the array and calls
 * hardware_interface__msg__BuzzerDuty__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_hardware_interface
hardware_interface__msg__BuzzerDuty__Sequence *
hardware_interface__msg__BuzzerDuty__Sequence__create(size_t size);

/// Destroy array of msg/BuzzerDuty messages.
/**
 * It calls
 * hardware_interface__msg__BuzzerDuty__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_hardware_interface
void
hardware_interface__msg__BuzzerDuty__Sequence__destroy(hardware_interface__msg__BuzzerDuty__Sequence * array);

/// Check for msg/BuzzerDuty message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_hardware_interface
bool
hardware_interface__msg__BuzzerDuty__Sequence__are_equal(const hardware_interface__msg__BuzzerDuty__Sequence * lhs, const hardware_interface__msg__BuzzerDuty__Sequence * rhs);

/// Copy an array of msg/BuzzerDuty messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_hardware_interface
bool
hardware_interface__msg__BuzzerDuty__Sequence__copy(
  const hardware_interface__msg__BuzzerDuty__Sequence * input,
  hardware_interface__msg__BuzzerDuty__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // HARDWARE_INTERFACE__MSG__DETAIL__BUZZER_DUTY__FUNCTIONS_H_
