import sys
import os

# make an output folder specific to this script
ext_loc = -(len(sys.argv[0]) - sys.argv[0].rindex('.'))
script_name = sys.argv[0][:ext_loc]
outdir = script_name + '_out'

os.makedirs(outdir, exist_ok = True)

from metadata import GlobalMetadataHeader

metadata_path = sys.argv[1]

strlit_outf = os.path.join(outdir, 'string_literals.txt')
cstr_outf = os.path.join(outdir, 'c_strings.txt')

def main():
  metadata = GlobalMetadataHeader.load(metadata_path)
  
  print('String Literals Section Offset: 0x%08x' % metadata.string_literal_offset)
  print('String Literals Section Size: %d bytes' % metadata.string_literal_size)
  
  print('String Literals Data Section Offset: 0x%08x'
    % metadata.string_literal_data_offset)
  print('String Literals Data Section Size: %d bytes'
    % metadata.string_literal_data_size)
  
  print('C Strings Section Offset: 0x%08x' % metadata.string_offset)
  print('C Strings Section Size: %d bytes' % metadata.string_size)
  
  print('-' * 24)
  
  with open(strlit_outf, 'w') as out_fobj:
    print("Writing string literals to '%s'..." % strlit_outf)
    
    for strlit in metadata.string_literals():
      block = '[ID: %d] len: %d\nliteral offset: 0x%08x\ndata offset: 0x%08x\nhex_content: %s\ntext_content: %s\n\n'
      block = block % (
        strlit.info.data_index,
        strlit.info.length,
        strlit.info.offset,
        strlit.offset,
        strlit.data.hex(),
        strlit.text
      )
      
      out_fobj.write(block)
      out_fobj.flush()
  
  with open(cstr_outf, 'w') as out_fobj:
    print("Writing c strings to '%s'..." % cstr_outf)
    
    index = 0
    for cstring in metadata.c_strings():
      block = '[#%d] len: %d\noffset: 0x%08x\nhex content: %s\ntext content: %s\n\n'
      block = block % (
        index,
        len(cstring.data),
        cstring.offset,
        cstring.data.hex(),
        cstring.text
      )
      
      out_fobj.write(block)
      out_fobj.flush()
      
      index += 1

main()