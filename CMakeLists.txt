cmake_minimum_required(VERSION 3.5)

project(pylc3.core VERSION 0.1 LANGAUGES CXX)

find_package(PythonExtensions REQUIRED)
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(Boost COMPONENTS python REQUIRED)
find_package(liblc3 REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})
include_directories(${Python3_INCLUDE_DIRS})
include_directories(${LIBLC3_INCLUDE_DIR})
link_directories(${Boost_LIBRARY_DIR})

set(CASTXML_PATH "/usr/bin/castxml" CACHE STRING "where to find the castXML executable")
set(CMAKE_SHARED_LINKER_FLAGS "-Wl,--export-all-symbols")

add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/PyLC3Gen.cpp ${CMAKE_CURRENT_BINARY_DIR}/exposed_decl.pypp.txt ${CMAKE_CURRENT_BINARY_DIR}/named_tuple.py
    COMMAND ${Python3_EXECUTABLE} scripts/pylc3_generator.py ${CASTXML_PATH}
    DEPENDS pylc3.core/PyLC3.hpp
    MAIN_DEPENDENCY scripts/pylc3_generator.py
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generating PyLC3Gen.cpp"
)

set(SRC_PYLC3
    pylc3.core/PyLC3.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/PyLC3Gen.cpp
)

add_library(
    pylc3.core
    MODULE
    ${SRC_PYLC3}
)

target_link_libraries(
    pylc3.core
    ${LIBLC3_LIBRARY}
    ${Boost_LIBRARIES}
    ${Python3_LIBRARIES}
)

set_target_properties(pylc3 PROPERTIES SUFFIX .so)
set_target_properties(pylc3 PROPERTIES PREFIX "")


python_extension_module(pylc3.core)

install(TARGETS pylc3.core LIBRARY DESTINATION pylc3.core)
