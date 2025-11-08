// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from hardware_interface:msg/BuzzerDuty.idl
// generated code does not contain a copyright notice

#ifndef HARDWARE_INTERFACE__MSG__DETAIL__BUZZER_DUTY__BUILDER_HPP_
#define HARDWARE_INTERFACE__MSG__DETAIL__BUZZER_DUTY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "hardware_interface/msg/detail/buzzer_duty__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace hardware_interface
{

namespace msg
{

namespace builder
{

class Init_BuzzerDuty_duty_cycle
{
public:
  Init_BuzzerDuty_duty_cycle()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::hardware_interface::msg::BuzzerDuty duty_cycle(::hardware_interface::msg::BuzzerDuty::_duty_cycle_type arg)
  {
    msg_.duty_cycle = std::move(arg);
    return std::move(msg_);
  }

private:
  ::hardware_interface::msg::BuzzerDuty msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::hardware_interface::msg::BuzzerDuty>()
{
  return hardware_interface::msg::builder::Init_BuzzerDuty_duty_cycle();
}

}  // namespace hardware_interface

#endif  // HARDWARE_INTERFACE__MSG__DETAIL__BUZZER_DUTY__BUILDER_HPP_
