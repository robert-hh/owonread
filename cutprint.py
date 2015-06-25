#
# Decode the fulldata header
#
# C-Equivalent:
#
# #pragma pack(1)

# struct cutdata_header {
   # char file_tag[6];
   # int32_t file_size;
   # int32_t flag_1;
   # int16_t real_time;
   # int16_t data_valid;
   # int32_t sample_rate_index;
   # int32_t storage_select;
   # int16_t data_mode;
   # int16_t no_of_channels;
   # int16_t channel_numbers[4];
   # int32_t vert_scale_index[4];
   # int32_t vert_offset[4];
   # int32_t vert_scale_index_dup[4];
   # int32_t vert_offset_dup[4];
   # int32_t scaling_factor_1[4];
   # int32_t time_stamp[4];
   # int32_t flag_2[4];
   # int32_t hor_scale_index;
   # int32_t flag_3;
   # float scroll_time;
   # float after_trigger_time;
   # float trigger_time;
   # float sample_interval;
   # float conversion_time;
   # float scaling_factor_2[4];
   # int32_t record_len;
   # int32_t wave_len;
   # int16_t probe_scale[4];
   # int32_t extraction_no;
   # int32_t data_offset[4];
   # int32_t no_math_facors;
   # int32_t flag_4;
   # int32_t math_length;
   # int32_t math_offset;
   # uint8_t math_data_desc[32];
# } header;

from struct import unpack, calcsize

def unpack_n_move(fmt, buf, index):
    flen = calcsize(fmt)
    return index + flen, unpack(fmt, buf[index:index + flen])

def decode_cutdata_hdr(buf):

    index = 0
    index, (file_tag, file_size, flag_1, real_time, data_valid, \
            sample_rate_index, storage_select, data_mode, \
            no_of_channels)         = unpack_n_move("<6sllhhllhh", buf, index)
    index, channel_numbers          = unpack_n_move("<hhhh", buf, index)
    index, verticle_scale_index     = unpack_n_move("<llll", buf, index)
    index, verticle_offset          = unpack_n_move("<llll", buf, index)
    index, verticle_scale_index_dup = unpack_n_move("<llll", buf, index)
    index, verticle_offset_dup      = unpack_n_move("<llll", buf, index)
    index, scaling_factor_1         = unpack_n_move("<llll", buf, index)
    index, time_stamp               = unpack_n_move("<llll", buf, index)
    index, flag2                    = unpack_n_move("<llll", buf, index)
    index, (hor_scale_index, flag3) = unpack_n_move("<ll", buf, index)
    index, (scroll_time, after_trigger_time, trigger_time, sample_interval, \
           conversion_time)         = unpack_n_move("<fffff", buf, index)
    index, scaling_factor_2         = unpack_n_move("<ffff", buf, index)
    index, (record_len, wave_len)   = unpack_n_move("<ll", buf, index)
    index, probe_scale              = unpack_n_move("<hhhh", buf, index)
    index, extraction_no            = unpack_n_move("<l", buf, index)
    index, data_offset              = unpack_n_move("<llll", buf, index)
    index, (no_math_facors, flag_4, math_length, math_offset) \
                                    = unpack_n_move("<llll", buf, index)
    index, math_data_desc           = unpack_n_move("<32s", buf, index)


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

# vert_scale_table units are mv 2 - 10000
    vert_scale_table = (2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000)

    print (file_tag, "File Tag")
    print (file_size, "File Size")
    print (flag_1, "Purpose Unknown")
    print (real_time, "Real-Time Flag")
    print (data_valid, "Data Valid")
    print (sample_rate_index, "Sample Rate Index, 2 GS/s = 0")
    print (sample_rate_table[sample_rate_index], "Sample Rate (by Index)" )
    if extraction_no[0] > 1:
        sample_rate = extraction_no[0]/sample_interval*500000
    else:
        sample_rate = extraction_no[0]/sample_interval*1000000
    print (sample_rate, "Sample rate (alt.)")
    print (storage_select, "Storage Select")
    print (data_mode, "Data Mode 0=normal, 1 = roll")
    print (no_of_channels, "# of Channels")
    for i in range(no_of_channels): 
        print (channel_numbers[i], "Channel Number %d" % (i + 1))
    print (hor_scale_index, "Horiz Scale Index, 2 ns/div = 1")
    print (hor_scale_table[hor_scale_index], "µs/div Horiz Scale)")
    print (verticle_scale_index, "Vertical Scale Index, 2 mV/Div = 0 ")
    for i in range(4): 
        print (vert_scale_table[verticle_scale_index[i]] * probe_scale[i] \
            / 1000.0, "V/div Vertical Scale %d" % i)
    print (verticle_offset,"Vertical Offset, 25 pt/div")  
    for i in range(4): 
        print (verticle_offset[i] * vert_scale_table[verticle_scale_index[i]] \
            * probe_scale[i] / 25000.0,"V Vertical Offset %d" % i)  
    print (scroll_time, "roll position Time")
    print (after_trigger_time, "Trigger Position Time 1 µs")
    print (trigger_time, "Trigger Position Time 2 µs")
    print (sample_interval, "ADC time per point µs")
    print (conversion_time, "ADC Conversion Time µs")
    print (record_len, "Record Length")
    print (wave_len, "Waveform Quantity")
    for i in range(4): 
        print (probe_scale[i], "Probe attenuation %d" % i)
    print (extraction_no[0], "fpga-extraction")
    for i in range(4): 
        print (data_offset[i], "Data offset %d" % i)

if __name__ == "__main__":
    import sys
    
    f = sys.stdin
    b = f.buffer.read(278)

 
    decode_cutdata_hdr(b)


