#/home/oz_computron/MCDTH/mctdh86.7/bin/binary/x86_64/autospec86 -o H1_spec_cc.pl -f ACF_ABS_CC_test_H1_A1_N3_normalized.txt -p 8000 5 15 ev 30 1 
set terminal png size 1200,800
set output '/home/oz_computron/Desktop/Research_idea/mixed_reprsentation/t-amplitudes-8171b20377162cf3b704c0d83f7eeae58bcbfdb5/H2_Z3_div_comp.png' 
set nologscale
set xzeroaxis
set xlabel 'Energy [eV]'
set xr [ 17: 13]
set yr [ 0: 40]
set title 'H_{2} Spectra, n-cos = 1, tau: 30.0 1, 200fs'
plot '/home/oz_computron/Desktop/Research_idea/mixed_reprsentation/t-amplitudes-8171b20377162cf3b704c0d83f7eeae58bcbfdb5/MCTDH_h2o_H2_converged.pl' using 1:2 with lines ls 2 lc 'red' title 'MCTDH',\
'/home/oz_computron/Desktop/Research_idea/mixed_reprsentation/t-amplitudes-8171b20377162cf3b704c0d83f7eeae58bcbfdb5/h2o_H2_Z3_div2.pl' using 1:2 with lines ls 2 lc 'black' title 'div 2 CC',\
#'/home/oz_computron/Desktop/Research_idea/mixed_reprsentation/t-amplitudes-8171b20377162cf3b704c0d83f7eeae58bcbfdb5/h2o_H2_Z1.pl' using 1:2 with lines ls 2 lc 'black' title 'CC'
