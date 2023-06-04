import struct
import sys
import os
import pprint

# make an output folder specific to this script
ext_loc = -(len(sys.argv[0]) - sys.argv[0].rindex('.'))
script_name = sys.argv[0][:ext_loc]

outdir = script_name + '_out'

os.makedirs(outdir, exist_ok = True)

metadata_path = sys.argv[1]
endianness = '<' # swap accordingly. little by default

strlit_outf = os.path.join(outdir, 'string_literals.txt')
cstr_outf = os.path.join(outdir, 'c_strings.txt')

def main():
  with open(metadata_path, 'rb') as metadata_fobj:
    def unpack(fmt):
      fmt = endianness + fmt
      
      return struct.unpack(fmt, metadata_fobj.read(struct.calcsize(fmt)))[0]
    
    # sanity check
    if unpack('I') != 0xFAB11BAF:
      print('Failed sanity check.')
      sys.exit(1)
    
    print('Version: %d' % (dataver := unpack('I')))
    
    if dataver != 29:
      # bring this to the user's attention
      print('Warning: this script was written for metadata version 29.')
      input('Press any key to continue dumping.')
    
    print('String Literals Offset: 0x%08x' % (strlit_off := unpack('I')))
    print('String Literals End: 0x%08x' % (strlit_end := unpack('I')))
    
    print('String Literals Data Offset: 0x%08x' % (strdat_off := unpack('I')))
    print('String Literals End: 0x%08x' % (strdat_end := unpack('I')))
    
    print('C Strings Offset: 0x%08x' % (cstr_off := unpack('I')))
    print('C Strings End: 0x%08x' % (cstr_end := unpack('I')))
    
    print('-' * 24)
    
    metadata_fobj.seek(strlit_off)
    with open(strlit_outf, 'w') as out_fobj:
      print("Writing string literals to '%s'..." % strlit_outf)
      
      literals = []
      while metadata_fobj.tell() != (strlit_end + 0x100):
        literals.append({
          'offset': metadata_fobj.tell(),
          'length': unpack('I'),
          'dataIndex': unpack('I')
        })
      
      # allocate some space on the screen to display progress
      print(' ' * 30, end = '')
      for lit in literals:
        # yikes, sadly i cant think of a way to move this call
        # out of here for now.
        metadata_fobj.seek(strdat_off + lit['dataIndex'])
        
        print('\rIndex: %d' % lit['dataIndex'], end = '')
        
        block = '[ID: %d] len: %d\nliteral offset: 0x%08x\ndata offset: 0x%08x\nhex_content: %s\ntext_content: %s\n\n'
        
        data_off = metadata_fobj.tell()
        content = metadata_fobj.read(lit['length'])
        text_content = content.decode('utf-8', 'backslashreplace')
        
        block = block % (
          lit['dataIndex'],
          lit['length'],
          lit['offset'],
          data_off,
          content.hex(),
          text_content
        )
        
        out_fobj.write(block)
        out_fobj.flush()
      
      print("\nDone")
    
    metadata_fobj.seek(cstr_off)
    with open(cstr_outf, 'w') as out_fobj:
      print("Writing c strings to '%s'..." % cstr_outf)
      
      i = 0
      print(' ' * 30, end = '')
      while metadata_fobj.tell() != (cstr_off + cstr_end):
        block = '[#%d] len: %d\noffset: 0x%08x\nhex content: %s\ntext content: %s\n\n'
        offset = metadata_fobj.tell()
        
        byte = None
        buff = bytearray()
        while byte != 0x00:
          byte = metadata_fobj.read(1)[0]
          
          buff.append(byte)
        i += 1
        
        print('\rCount: %d' % i, end = '')
        
        text_content = buff.decode('utf-8', 'backslashreplace')
        
        block = block % (
          i,
          len(buff),
          offset,
          buff.hex(),
          text_content
        )
        
        out_fobj.write(block)
        out_fobj.flush()
      
      print("\nDone")

main()