// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from hardware_interface:msg/BuzzerDuty.idl
// generated code does not contain a copyright notice

#ifndef HARDWARE_INTERFACE__MSG__DETAIL__BUZZER_DUTY__TRAITS_HPP_
#define HARDWARE_INTERFACE__MSG__DETAIL__BUZZER_DUTY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "hardware_interface/msg/detail/buzzer_duty__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace hardware_interface
{

namespace msg
{

inline void to_flow_style_yaml(
  const BuzzerDuty & msg,
  std::ostream & out)
{
  out << "{";
  // member: duty_cycle
  {
    out << "duty_cycle: ";
    rosidl_generator_traits::value_to_yaml(msg.duty_cycle, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const BuzzerDuty & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: duty_cycle
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "duty_cycle: ";
    rosidl_generator_traits::value_to_yaml(msg.duty_cycle, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const BuzzerDuty & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace hardware_interface

namespace rosidl_generator_traits
{

[[deprecated("use hardware_interface::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const hardware_interface::msg::BuzzerDuty & msg,
  std::ostream & out, size_t indentation = 0)
{
  hardware_interface::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use hardware_interface::msg::to_yaml() instead")]]
inline std::string to_yaml(const hardware_interface::msg::BuzzerDuty & msg)
{
  return hardware_interface::msg::to_yaml(msg);
}

template<>
inline const char * data_type<hardware_interface::msg::BuzzerDuty>()
{
  return "hardware_interface::msg::BuzzerDuty";
}

template<>
inline const char * name<hardware_interface::msg::BuzzerDuty>()
{
  return "hardware_interface/msg/BuzzerDuty";
}

template<>
struct has_fixed_size<hardware_interface::msg::BuzzerDuty>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<hardware_interface::msg::BuzzerDuty>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<hardware_interface::msg::BuzzerDuty>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // HARDWARE_INTERFACE__MSG__DETAIL__BUZZER_DUTY__TRAITS_HPP_
