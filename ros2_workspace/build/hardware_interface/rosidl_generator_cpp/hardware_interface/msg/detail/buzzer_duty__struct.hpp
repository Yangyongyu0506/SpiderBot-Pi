// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from hardware_interface:msg/BuzzerDuty.idl
// generated code does not contain a copyright notice

#ifndef HARDWARE_INTERFACE__MSG__DETAIL__BUZZER_DUTY__STRUCT_HPP_
#define HARDWARE_INTERFACE__MSG__DETAIL__BUZZER_DUTY__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__hardware_interface__msg__BuzzerDuty __attribute__((deprecated))
#else
# define DEPRECATED__hardware_interface__msg__BuzzerDuty __declspec(deprecated)
#endif

namespace hardware_interface
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct BuzzerDuty_
{
  using Type = BuzzerDuty_<ContainerAllocator>;

  explicit BuzzerDuty_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->duty_cycle = 0;
    }
  }

  explicit BuzzerDuty_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->duty_cycle = 0;
    }
  }

  // field types and members
  using _duty_cycle_type =
    uint8_t;
  _duty_cycle_type duty_cycle;

  // setters for named parameter idiom
  Type & set__duty_cycle(
    const uint8_t & _arg)
  {
    this->duty_cycle = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    hardware_interface::msg::BuzzerDuty_<ContainerAllocator> *;
  using ConstRawPtr =
    const hardware_interface::msg::BuzzerDuty_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<hardware_interface::msg::BuzzerDuty_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<hardware_interface::msg::BuzzerDuty_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      hardware_interface::msg::BuzzerDuty_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<hardware_interface::msg::BuzzerDuty_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      hardware_interface::msg::BuzzerDuty_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<hardware_interface::msg::BuzzerDuty_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<hardware_interface::msg::BuzzerDuty_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<hardware_interface::msg::BuzzerDuty_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__hardware_interface__msg__BuzzerDuty
    std::shared_ptr<hardware_interface::msg::BuzzerDuty_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__hardware_interface__msg__BuzzerDuty
    std::shared_ptr<hardware_interface::msg::BuzzerDuty_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const BuzzerDuty_ & other) const
  {
    if (this->duty_cycle != other.duty_cycle) {
      return false;
    }
    return true;
  }
  bool operator!=(const BuzzerDuty_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct BuzzerDuty_

// alias to use template instance with default allocator
using BuzzerDuty =
  hardware_interface::msg::BuzzerDuty_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace hardware_interface

#endif  // HARDWARE_INTERFACE__MSG__DETAIL__BUZZER_DUTY__STRUCT_HPP_
