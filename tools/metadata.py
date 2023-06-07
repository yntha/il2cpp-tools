import struct
import io
import json

from dataclasses import dataclass

@dataclass
class MetadataItem:
  offset: int

@dataclass
class StringLiteralInfo(MetadataItem):
  length: int
  data_index: int

@dataclass
class StringLiteral(MetadataItem):
  info: StringLiteralInfo
  data: bytes
  text: str

@dataclass
class CString(MetadataItem):
  data: bytes
  text: str

class Il2CppClass:
  def __init__(self):
    self.image = None
    self.gc_desc = None
    self.name = None
    self.namespaze = None
    self.byval_arg = None
    self.this_arg = None
    self.element_class = None
    self.cast_class = None
    self.declaring_type = None
    self.parent = None
    self.generic_class = None
    self.type_metadata_handle = None
    self.interop_data = None
    self.klass = None
    self.fields = None
    self.events = None
    self.properties = None
    self.methods = None
    self.nested_types = None
    self.implemented_interfaces = None
    self.interface_offsets = None
    self.static_fields = None
    self.rgctx_data = None
    self.type_hierarchy = None
    self.unity_user_data = None
    self.initialization_exception_gc_handle = None
    self.cctor_started = None
    self.cctor_finished_or_no_cctor = None
    self.cctor_thread = None
    self.generic_container_handle = None
    self.instance_size = None
    self.stack_slot_size = None
    self.actual_size = None
    self.element_size = None
    self.native_size = None
    self.static_fields_size = None
    self.thread_static_fields_size = None
    self.thread_static_fields_offset = None
    self.flags = None
    self.token = None
    self.method_count = None
    self.property_count = None
    self.field_count = None
    self.event_count = None
    self.nested_type_count = None
    self.vtable_count = None
    self.interfaces_count = None
    self.interface_offsets_count = None
    self.type_hierarchy_depth = None
    self.generic_recursion_depth = None
    self.rank = None
    self.minimum_alignment = None
    self.packing_size = None
    self.initialized_and_no_error = None
    self.initialized = None
    self.enumtype = None
    self.nullabletype = None
    self.is_generic = None
    self.has_references = None
    self.init_pending = None
    self.size_init_pending = None
    self.size_inited = None
    self.has_finalize = None
    self.has_cctor = None
    self.is_blittable = None
    self.is_import_or_windows_runtime = None
    self.is_vtable_initialized = None
    self.is_byref_like = None
    self.vtable = None

class GlobalMetadataHeader:
  noload = [
    'file_path',
    'byte_order',
    'noload',
    'methods',
    'strings',
    'cstrings',
    'virtual_methods'
  ]
  
  def __init__(self, metadata_path, byte_order = '<'):
    self.file_path = metadata_path
    self.byte_order = byte_order
    
    self.strings = None
    self.cstrings = None
    self.methods = None
    self.properties = None
    self.virtual_methods = None
    
    self.sanity = None
    self.version = None
    self.string_literal_offset = None
    self.string_literal_size = None
    self.string_literal_data_offset = None
    self.string_literal_data_size = None
    self.string_offset = None
    self.string_size = None
    self.events_offset = None
    self.events_size = None
    self.properties_offset = None
    self.properties_size = None
    self.methods_offset = None
    self.methods_size = None
    self.parameter_default_values_offset = None
    self.parameter_default_values_size = None
    self.field_default_values_offset = None
    self.field_default_values_size = None
    self.field_and_parameter_default_value_data_offset = None
    self.field_and_parameter_default_value_data_size = None
    self.field_marshaled_sizes_offset = None
    self.field_marshaled_sizes_size = None
    self.parameters_offset = None
    self.parameters_size = None
    self.fields_offset = None
    self.fields_size = None
    self.generic_parameters_offset = None
    self.generic_parameters_size = None
    self.generic_parameter_constraints_offset = None
    self.generic_parameter_constraints_size = None
    self.generic_containers_offset = None
    self.generic_containers_size = None
    self.nested_types_offset = None
    self.nested_types_size = None
    self.interfaces_offset = None
    self.interfaces_size = None
    self.vtable_methods_offset = None
    self.vtable_methods_size = None
    self.interface_offsets_offset = None
    self.interface_offsets_size = None
    self.type_definitions_offset = None
    self.type_definitions_size = None
    self.images_offset = None
    self.images_size = None
    self.assemblies_offset = None
    self.assemblies_size = None
    self.field_refs_offset = None
    self.field_refs_size = None
    self.referenced_assemblies_offset = None
    self.referenced_assemblies_size = None
    self.attribute_data_offset = None
    self.attribute_data_size = None
    self.attribute_data_range_offset = None
    self.attribute_data_range_size = None
    self.unresolved_indirect_call_parameter_types_offset = None
    self.unresolved_indirect_call_parameter_types_size = None
    self.unresolved_indirect_call_parameter_ranges_offset = None
    self.unresolved_indirect_call_parameter_ranges_size = None
    self.windows_runtime_type_names_offset = None
    self.windows_runtime_type_names_size = None
    self.windows_runtime_strings_offset = None
    self.windows_runtime_strings_size = None
    self.exported_type_definitions_offset = None
    self.exported_type_definitions_size = None
  
  @classmethod
  def load(cls, path):
    instance = cls(path)
    
    with open(path, 'rb') as metadata_fobj:
      for k in instance.__dict__:
        if k in cls.noload:
          continue
        
        v = instance._unpack('I', metadata_fobj)
        
        if k == 'sanity' and v != 0xFAB11BAF:
          print('Failed sanity check.')
          
          return None
        
        if k == 'version' and v != 29:
          print('Warning: only metadata v29 is supported.')
          input('Press any key to continue loading...')
        
        setattr(instance, k, v)
    
    return instance
  
  def _unpack(self, fmt, fobj):
    fmt = self.byte_order + fmt
    
    return struct.unpack(fmt, fobj.read(struct.calcsize(fmt)))[0]
  
  def methods(self):
    with open(self.file_path, 'rb') as metadata_fobj:
      metadata_fobj.seek(self.string_literal_offset)
      
      
  
  def virtual_methods(self):
    pass
  
  def properties(self):
    pass
  
  def _fetch_strlit_info(self):
    with open(self.file_path, 'rb') as metadata_fobj:
      metadata_fobj.seek(self.string_literal_offset)
      
      end = self.string_literal_offset + self.string_literal_size
      while metadata_fobj.tell() <= end:
        yield StringLiteralInfo(
          metadata_fobj.tell(),
          self._unpack('I', metadata_fobj),
          self._unpack('i', metadata_fobj)
        )
  
  def string_literals(self):
    with open(self.file_path, 'rb') as metadata_fobj:
      for litinfo in self._fetch_strlit_info():
        metadata_fobj.seek(self.string_literal_data_offset + litinfo.data_index)
        
        offset = metadata_fobj.tell()
        data = metadata_fobj.read(litinfo.length)
        
        yield StringLiteral(
          offset,
          litinfo,
          data,
          data.decode('utf-8', 'backslashreplace')
        )
  
  def c_strings(self):
    with open(self.file_path, 'rb') as metadata_fobj:
      metadata_fobj.seek(self.string_offset)
      
      end = self.string_offset + self.string_size
      while metadata_fobj.tell() <= end:
        offset = metadata_fobj.tell()
        
        byte = None
        buff = bytearray()
        while byte != 0x00:
          byte = metadata_fobj.read(1)[0]
          
          buff.append(byte)
        
        yield CString(
          offset,
          bytes(buff),
          buff.decode('utf-8', 'backslashreplace')
        )
  
  def __repr__(self):
    return json.dumps(self.__dict__, indent = 2)