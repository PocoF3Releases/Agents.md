ENTRY(_start)
SECTIONS { . = 0x400000; .entry : { *(.entry) } . = 0x79d3b8; .site : { *(.site) } . = 0x8c0640; .guard : { *(.guard) } . = 0x900000; .data : { *(.data) } }
