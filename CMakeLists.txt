cmake_minimum_required(VERSION 3.5)

project(pylc3.core LANGUAGES CXX VERSION 0.1)

set(CASTXML_PATH "/usr/bin/castxml" CACHE STRING "where to find the castXML executable")

find_package(PythonExtensions REQUIRED)
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(Boost COMPONENTS python REQUIRED)
find_package(liblc3 REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})
include_directories(${Python3_INCLUDE_DIRS})
include_directories(${LIBLC3_INCLUDE_DIR})
link_directories(${Boost_LIBRARY_DIR})

# Require C++11 build
if(NOT CMAKE_CXX_FLAGS MATCHES "-std=(c|gnu)\\+\\+11")
    message(STATUS "This project requires C++11. Adding -std=c++11 to CXXFLAGS.")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11" CACHE STRING "Flags used by the compiler during all build types." FORCE)
endif()

# Additional debug flags
set(CMAKE_CXX_FLAGS_DEBUG "-g -pg")
set(CMAKE_DEBUG_POSTFIX d)

# Set default warning flags
set(PROJECT_WARNING_FLAGS "-Wall -Wno-deprecated -Wno-deprecated-declarations" CACHE STRING "Compiler warning flags to include")
mark_as_advanced(PROJECT_WARNING_FLAGS)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${PROJECT_WARNING_FLAGS}")

if(ENABLE_COVERAGE)
    include(CodeCoverage)
    append_coverage_compiler_flags()
endif(ENABLE_COVERAGE)

# Default to release build if not specified
if(NOT CMAKE_BUILD_TYPE)
    message(STATUS "Setting build type to 'Release' as none was specified.")
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release"
    "MinSizeRel" "RelWithDebInfo")
endif(NOT CMAKE_BUILD_TYPE)

if(CMAKE_BUILD_TYPE MATCHES "Debug")
    set(CMAKE_EXE_LINKER_FLAGS "-fprofile-arcs -ftest-coverage")
endif(CMAKE_BUILD_TYPE MATCHES "Debug")

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

set_target_properties(pylc3.core PROPERTIES SUFFIX .so)
set_target_properties(pylc3.core PROPERTIES PREFIX "")

python_extension_module(pylc3.core)

install(TARGETS pylc3.core LIBRARY DESTINATION pylc3.core)
