#/home/oz_computron/MCDTH/mctdh86.7/bin/binary/x86_64/autospec86 -o H1_spec_cc.pl -f ACF_ABS_CC_test_H1_A1_N3_normalized.txt -p 8000 5 15 ev 30 1 
set terminal png size 1200,800
set output '/home/oz_computron/Desktop/Research_idea/mixed_reprsentation/t-amplitudes-8171b20377162cf3b704c0d83f7eeae58bcbfdb5/mctdh_h2o_H1_S1_Z1.png' 
set nologscale
set xzeroaxis
set xlabel 'Energy [eV]'
set xr [ 20: 10]
set yr [ 0: 40]
set title 'H_{0} Spectra, n-cos = 1, tau: 30.0 1, 200fs'
plot '/home/oz_computron/Desktop/Research_idea/mixed_reprsentation/t-amplitudes-8171b20377162cf3b704c0d83f7eeae58bcbfdb5/mctdh_h2o_H1_S1_Z1.pl' using 1:2 with lines ls 2 lc 'black' title 'MCTDH'
#'/home/oz_computron/Desktop/Research_idea/project-violence/t0veccpro_working/workspace/ACF_ABS_CC_H1_A1_N3_normalized.pl' using 1:2 with lines ls 2 lc 'red' title 'CC' 
