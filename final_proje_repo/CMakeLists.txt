cmake_minimum_required(VERSION 3.0.2)
project(final_proje_repo)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  sensor_msgs
  geometry_msgs
)

catkin_package()
