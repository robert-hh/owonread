#
# Decode the fulldata header
#
# C-Equivalent:
#
# struct fulldata_header {
#    char file_tag[6];
#    int32_t file_size;
#    int32_t flag_1;
#    int16_t real_time;
#    int16_t data_valid;
#    int32_t sample_rate_index;
#    int32_t storage_select;
#    int16_t data_mode;
#    int16_t hor_scale_index;
#    int32_t vert_scale_index;
#    int32_t vert_offset;
#    float scroll_time;
#    float after_trigger_time;
#    float trigger_time;
#    float sample_interval;
#    float conversion_time;
#    int32_t record_length;
#    int32_t ADC_length;
#    int16_t probe_scale;
#    int32_t extraction_no;
#    int32_t data_offset;
# }

def decode_fulldata_hdr(buf):

    from struct import unpack

    fmt = "<6sllhhllhhllffffflllll"

    file_tag, file_size, flag_1, real_time, data_valid, sample_rate_index, \
    storage_select, data_mode, hor_scale_index, vert_scale_index, vert_offset,\
    scroll_time, after_trigger_time, trigger_time, sample_interval, \
    conversion_time, record_length, storage_length, probe_scale, extraction_no, \
    data_offset  = unpack(fmt, buf[0:78])

# sample rate table units are samples/s (range 2000000000 downto 5)
    sample_rate_table = \
    (2000000000, 1000000000, 500000000, 250000000, 100000000, \
    50000000, 25000000, 10000000, 5000000, 2500000, 1000000, \
    500000, 250000, 100000, 50000, 25000, 10000, 5000, 2500, \
    1000, 500, 250, 100, 50, 25, 10, 5)

# hor_scale table units are µs (range 0.001 to 100000 )
    hor_scale_table = \
    (0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, \
    2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, \
    1.0e3, 2.0e3, 5.0e3, 10.0e3, 20.0e3, 50.0e3, 100.0e3, 200.0e3,  500.0e3, \
    1.0e6, 2.0e6, 5.0e6, 10.0e6, 20.0e6, 50.0e6, 100.0e6)

# ver_scale_table units are mv 2 - 10000
    vert_scale_table = (2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000)

    print (file_tag, "File Tag")
    print (file_size, "File Size")
    print (flag_1, "Purpose Unknown")
    print (real_time, "Real-Time Flag")
    print (data_valid, "Data Valid")
    print (sample_rate_index, "Sample Rate Index, 2 GS/s = 0")
    print (sample_rate_table[sample_rate_index], "Sample Rate")
    print (storage_select, "Storage Select")
    print (data_mode, "Data Mode 0=normal, 1 = roll")
    print (hor_scale_index, "Horiz Scale Index, 2 ns/div = 1")
    print (hor_scale_table[hor_scale_index], "µs /div Horiz Scale)")
    print (vert_scale_index, "Vertical Scale Index, 2 mV/Div = 0 ")
    print (vert_scale_table[vert_scale_index] * probe_scale, "mv/div Vertical Scale")
    print (vert_offset * vert_scale_table[vert_scale_index] * probe_scale / 25,"mV Vertical Offset")  
    print (vert_offset,"Vertical Offset, 25 pt/div")  
    print (scroll_time, "roll position Time")
    print (after_trigger_time, "Trigger Position Time 1 µs")
    print (trigger_time, "Trigger Position Time 2 µs")
    print (sample_interval, "ADC time per point µs")
    print (conversion_time, "ADC Convertion Time µs")
    print (record_length, "Record Length")
    print (storage_length, "Storage Length")
    print (probe_scale, "Probe attenuation")
    print (extraction_no, "fpga-extraction")
    print (data_offset, "Data offset")

if __name__ == "__main__":
    import sys

    f = sys.stdin

    b = f.buffer.read(78)

    decode_fulldata_hdr(b)


