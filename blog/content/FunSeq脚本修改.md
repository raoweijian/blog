FunSeq是 gersteinlab 开发的一个进行变异注释的软件，专注于非编码区注释，详细介绍见 funseq.gersteinlab.org。

但是在使用这个软件的过程中，有一些问题：

##问题1：
如果输入为BED格式，并且设置了进行 coding 分析，在输出结果中，coding 区的 variant 会丢失一些信息（如下图）。

![](http://img.blog.csdn.net/20140410182715312?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcmFvd2Vpamlhbg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

原因：FUNSEQ.pm中 intergrate 函数中的 read_cds 函数在处理 bed 格式文件时，也对坐标进行了 -1 操作（该操作应该只对 vcf 格式文
件进行），所以在最后输出时，找不到相应存在哈希中的数据。

解决办法：修改 read_cds 函数，把文件格式作为参数给 read_cds， 并且在得到 $id 之前进行判断，BED格式不 -1， VCF 格式 -1。

    sub read_cds{
        my ($file, $format) = @_;
        open(IN,$file);
        while(<IN>){
          chomp $_;
          my @tmp = split /\t+/,$_;
          my $id;
          if($format =~ /bed/i){
            $id = join("\t",$tmp[0],$tmp[1]);
          }else{
            $id = join("\t",$tmp[0],$tmp[1]-1);
          }
          $id =~ s/chr//;

##问题2
如果输入为 VCF 格式，程序在生成中间文件时，不会把 VCF 的文件头输入进去。但是在随后调用 intersectBed 程序时，该程序会报错，大意是无法识别格式。

原因：intersectBed （v2.19.1）要求 VCF 格式的文件必须要有文件头的第一行。因此在程序生成中间文件后，还需用 sed 命令增加一行，如下：
`sed -i '1 i ##fileformat=VCFv4.1' $out_nc` if($informat =~ /vcf/i);


原始的程序默认使用多线程，即可以一次输入多个文件，以逗号隔开，然后多线程同时运算。考虑到该功能实用性未必好，如果投到集群上，没有申请足够的CPU也是没用的，因此去掉了多线程模块，只支持一次输入一个文件。
