#!/usr/bin/python3
import argparse
import os

from pygccxml import parser
from pygccxml import declarations
from pyplusplus import module_builder

import sys

parser = argparse.ArgumentParser(description="Generate bindings from header files")
parser.add_argument("--castxml_path", default="/usr/bin/castxml", type=str)
parser.add_argument("--pylc3_header")
parser.add_argument("--liblc3_include_path")
parser.add_argument("--output_path")
parser.add_argument("--compiler_path")

args = parser.parse_args()


# Create configuration for CastXML
xml_generator_config = parser.xml_generator_configuration_t(
                                    xml_generator_path=generator_path,
                                    xml_generator='castxml',
                                    compiler='gnu',
                                    compiler_path=args.compiler_path,
                                    cflags=f'-std=c++11 -I{args.liblc3_include_path}')

# List of all the C++ header of our library
header_collection = [args.pylc3_header, f"{args.liblc3_include_path}/lc3_all.hpp"]

# Parses the source files and creates a module_builder object
builder = module_builder.module_builder_t(
                        header_collection,
                        xml_generator_path=args.castxml_path,
                        xml_generator_config=xml_generator_config)

# Debugging
# builder.print_declarations()
#print dir(builder)

# Whitelist exporting of stuff.
builder.decls().exclude()

lc3_state = builder.class_('LC3State')
lc3_state.include()
builder.class_("lc3_breakpoint_info").include()
builder.class_("lc3_watchpoint_info").include()
builder.class_("lc3_blackbox_info").include()
builder.class_("lc3_subroutine_call_info").include()
builder.class_("lc3_trap_call_info").include()
builder.class_("lc3_memory_stats").include()
builder.enum("MemoryFillStrategy").include()

builder.decl("::std::vector<lc3_subroutine_call_info, std::allocator<lc3_subroutine_call_info> >").include()
builder.decl("::std::vector<lc3_trap_call_info, std::allocator<lc3_trap_call_info> >").include()
builder.decl("::std::map<unsigned short, lc3_blackbox_info, std::less<unsigned short>, std::allocator<std::pair<const unsigned short, lc3_blackbox_info> > >").include()
builder.decl("::std::map<unsigned short, lc3_breakpoint_info, std::less<unsigned short>, std::allocator<std::pair<const unsigned short, lc3_breakpoint_info> > >").include()
builder.decl("::std::map<unsigned short, lc3_watchpoint_info, std::less<unsigned short>, std::allocator<std::pair<const unsigned short, lc3_watchpoint_info> > >").include()
builder.decl("::std::map<unsigned short, lc3_memory_stats, std::less<unsigned short>, std::allocator<std::pair<const unsigned short, lc3_memory_stats> > >").include()



# Don't export accessors
builder.classes().add_properties(exclude_accessors=True)
# Enclude protected and private methods.
builder.calldefs(declarations.access_type_matcher_t('protected')).exclude()
builder.calldefs(declarations.access_type_matcher_t('private')).exclude()

# Define a name for the module
builder.build_code_creator(module_name="pylc3.core")

# Writes the C++ interface file
builder.write_module(os.path.join(args.output_path, 'PyLC3Gen.cpp'))
