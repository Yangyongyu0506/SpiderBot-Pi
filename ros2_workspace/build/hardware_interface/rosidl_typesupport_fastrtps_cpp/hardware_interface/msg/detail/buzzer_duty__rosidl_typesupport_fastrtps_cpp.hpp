// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from hardware_interface:msg/BuzzerDuty.idl
// generated code does not contain a copyright notice

#ifndef HARDWARE_INTERFACE__MSG__DETAIL__BUZZER_DUTY__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define HARDWARE_INTERFACE__MSG__DETAIL__BUZZER_DUTY__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "hardware_interface/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "hardware_interface/msg/detail/buzzer_duty__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace hardware_interface
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_hardware_interface
cdr_serialize(
  const hardware_interface::msg::BuzzerDuty & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_hardware_interface
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  hardware_interface::msg::BuzzerDuty & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_hardware_interface
get_serialized_size(
  const hardware_interface::msg::BuzzerDuty & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_hardware_interface
max_serialized_size_BuzzerDuty(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace hardware_interface

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_hardware_interface
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, hardware_interface, msg, BuzzerDuty)();

#ifdef __cplusplus
}
#endif

#endif  // HARDWARE_INTERFACE__MSG__DETAIL__BUZZER_DUTY__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
