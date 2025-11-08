// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from hardware_interface:msg/BuzzerDuty.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "hardware_interface/msg/detail/buzzer_duty__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace hardware_interface
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void BuzzerDuty_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) hardware_interface::msg::BuzzerDuty(_init);
}

void BuzzerDuty_fini_function(void * message_memory)
{
  auto typed_message = static_cast<hardware_interface::msg::BuzzerDuty *>(message_memory);
  typed_message->~BuzzerDuty();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember BuzzerDuty_message_member_array[1] = {
  {
    "duty_cycle",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(hardware_interface::msg::BuzzerDuty, duty_cycle),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers BuzzerDuty_message_members = {
  "hardware_interface::msg",  // message namespace
  "BuzzerDuty",  // message name
  1,  // number of fields
  sizeof(hardware_interface::msg::BuzzerDuty),
  BuzzerDuty_message_member_array,  // message members
  BuzzerDuty_init_function,  // function to initialize message memory (memory has to be allocated)
  BuzzerDuty_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t BuzzerDuty_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &BuzzerDuty_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace hardware_interface


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<hardware_interface::msg::BuzzerDuty>()
{
  return &::hardware_interface::msg::rosidl_typesupport_introspection_cpp::BuzzerDuty_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, hardware_interface, msg, BuzzerDuty)() {
  return &::hardware_interface::msg::rosidl_typesupport_introspection_cpp::BuzzerDuty_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
