import os
import subprocess
import struct

rootdir = './'

files = os.listdir(rootdir)
files.sort()

prefix = '''
var importObject = {
    env: {
        print_number: function (number) {
            print('[+] importObject callback.');
            print(number);
        }
    }
};
var wasmCode = new Uint8Array(['''

postfix = ''']);
///////////////////////////////////////////////////////////////////////////INIT
try {
    var wasmModule = new WebAssembly.Module(wasmCode);
    var wasmInstance = new WebAssembly.Instance(wasmModule, importObject);
    
    print('[+] wasmCode validate.');
    print(WebAssembly.validate(wasmCode));
}
catch (e) { print(e); }
///////////////////////////////////////////////////////////////////////////EXPORTS
try {
    var wasmInstanceExported = wasmInstance.exports;
    print('[+] wasmInstanceExported.');
    try{
        var wasmInstanceExportedTable = wasmInstance.exports.table;
        for(var i = 0;i < 100;i++){
            print(wasmInstanceExportedTable.get(i));
        }
    }
    catch(e){print(e);}

    try {
        print(wasmInstanceExported.main(0));
    }
    catch (e) { print(e);}

    try{
    for (var i in wasmInstanceExported) {
        try {
            print(eval('wasmInstanceExported.'+i+';'));
        }
        catch (e) { print(e);}
        try {
            print(eval('wasmInstanceExported.'+i+'(0);'));

        }
        catch (e) { print(e);}
    }
    }
    catch(e) {print(e);}


    var wasmModuleExports = WebAssembly.Module.exports(wasmModule);
    var varExports = [];
    print('[+] wasmModuleExported.')
    for(var i of wasmModuleExports){
        print(i+' : '+i.kind+' : '+i.name);
        varExports.push(i.name);
    }
    for(var i of varExports){
	try{
    	    print(eval('wasmInstanceExported.'+i+';'));
	}
	catch(e){print(e);}
	try{
            print(eval('wasmInstanceExported.'+i+'(0);'));
	}
	catch(e){print(e);}
    }    
}
catch (e) { print(e) };
///////////////////////////////////////////////////////////////////////////IMPORTS
try {
    var wasmModuleImports = WebAssembly.Module.imports(wasmModule);
    var varImports = [];
    print('[+] wasmModuleImported.')
    for(var i of wasmModuleImports){
        print(i+' : '+i.kind+' : '+i.name + ' : ' + i.module);
        varImports.push(i.name);
    }
}
catch (e) { print(e) };

/////////////////////////////////////////////////////////////////////////MEMORY
try {
    var wasmMemory = wasmInstance.exports.memory;
    print('[+] wasmMemory.');
    print(wasmMemory);
    print(wasmMemory instanceof WebAssembly.Memory);
}
catch (e) { print(e); }
////////////////////////////////////////////////////////////////////////
print("[+] End.");'''
count = -1

for i in range(0, len(files)):
	if (files[i].find('id:')!=-1) and (os.path.isdir(files[i])==False):
		count = count + 1
		print files[i]
		file_object = open(files[i])
		try:
			content = file_object.read()
			new_content = prefix
			for c in content:
				byte, = struct.unpack('B',c) 
				new_content += hex(byte) + ','
			new_content += postfix
			print new_content
			new_file = 'id' + str(count)
			with open(new_file, 'w') as f:
				f.write(new_content)
		finally:
			file_object.close()
			print '------------------------------'

