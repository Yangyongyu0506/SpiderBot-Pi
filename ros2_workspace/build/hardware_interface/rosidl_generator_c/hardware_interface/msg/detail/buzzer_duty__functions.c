// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from hardware_interface:msg/BuzzerDuty.idl
// generated code does not contain a copyright notice
#include "hardware_interface/msg/detail/buzzer_duty__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
hardware_interface__msg__BuzzerDuty__init(hardware_interface__msg__BuzzerDuty * msg)
{
  if (!msg) {
    return false;
  }
  // duty_cycle
  return true;
}

void
hardware_interface__msg__BuzzerDuty__fini(hardware_interface__msg__BuzzerDuty * msg)
{
  if (!msg) {
    return;
  }
  // duty_cycle
}

bool
hardware_interface__msg__BuzzerDuty__are_equal(const hardware_interface__msg__BuzzerDuty * lhs, const hardware_interface__msg__BuzzerDuty * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // duty_cycle
  if (lhs->duty_cycle != rhs->duty_cycle) {
    return false;
  }
  return true;
}

bool
hardware_interface__msg__BuzzerDuty__copy(
  const hardware_interface__msg__BuzzerDuty * input,
  hardware_interface__msg__BuzzerDuty * output)
{
  if (!input || !output) {
    return false;
  }
  // duty_cycle
  output->duty_cycle = input->duty_cycle;
  return true;
}

hardware_interface__msg__BuzzerDuty *
hardware_interface__msg__BuzzerDuty__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  hardware_interface__msg__BuzzerDuty * msg = (hardware_interface__msg__BuzzerDuty *)allocator.allocate(sizeof(hardware_interface__msg__BuzzerDuty), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(hardware_interface__msg__BuzzerDuty));
  bool success = hardware_interface__msg__BuzzerDuty__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
hardware_interface__msg__BuzzerDuty__destroy(hardware_interface__msg__BuzzerDuty * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    hardware_interface__msg__BuzzerDuty__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
hardware_interface__msg__BuzzerDuty__Sequence__init(hardware_interface__msg__BuzzerDuty__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  hardware_interface__msg__BuzzerDuty * data = NULL;

  if (size) {
    data = (hardware_interface__msg__BuzzerDuty *)allocator.zero_allocate(size, sizeof(hardware_interface__msg__BuzzerDuty), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = hardware_interface__msg__BuzzerDuty__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        hardware_interface__msg__BuzzerDuty__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
hardware_interface__msg__BuzzerDuty__Sequence__fini(hardware_interface__msg__BuzzerDuty__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      hardware_interface__msg__BuzzerDuty__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

hardware_interface__msg__BuzzerDuty__Sequence *
hardware_interface__msg__BuzzerDuty__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  hardware_interface__msg__BuzzerDuty__Sequence * array = (hardware_interface__msg__BuzzerDuty__Sequence *)allocator.allocate(sizeof(hardware_interface__msg__BuzzerDuty__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = hardware_interface__msg__BuzzerDuty__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
hardware_interface__msg__BuzzerDuty__Sequence__destroy(hardware_interface__msg__BuzzerDuty__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    hardware_interface__msg__BuzzerDuty__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
hardware_interface__msg__BuzzerDuty__Sequence__are_equal(const hardware_interface__msg__BuzzerDuty__Sequence * lhs, const hardware_interface__msg__BuzzerDuty__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!hardware_interface__msg__BuzzerDuty__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
hardware_interface__msg__BuzzerDuty__Sequence__copy(
  const hardware_interface__msg__BuzzerDuty__Sequence * input,
  hardware_interface__msg__BuzzerDuty__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(hardware_interface__msg__BuzzerDuty);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    hardware_interface__msg__BuzzerDuty * data =
      (hardware_interface__msg__BuzzerDuty *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!hardware_interface__msg__BuzzerDuty__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          hardware_interface__msg__BuzzerDuty__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!hardware_interface__msg__BuzzerDuty__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
