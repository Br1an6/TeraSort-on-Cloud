import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.*;

public class HadoopSort {

    public static void main(String[] arg) throws Exception{
        long start = System.currentTimeMillis();

        Configuration configuration = new Configuration();
        Job job = Job.getInstance(configuration, "Sort using Hadoop");

        /*Setting up Key,Value type class for output */
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        /*Setting up input and output paths for file to be sorted*/

        FileInputFormat.addInputPath(job, new Path(arg[0]));
        FileOutputFormat.setOutputPath(job, new Path(arg[1]));

        /*Setting up Mapper, Combiner, Reducer classes*/
        job.setJarByClass(HadoopSort.class);
        job.setMapperClass(MapperForSorting.class);
        job.setCombinerClass(ReducerForSorting.class);
        job.setReducerClass(ReducerForSorting.class);

        long end = System.currentTimeMillis();
        long timeTaken = end - start;

        if (job.waitForCompletion(true))
        {
            System.out.println("Time taken by Hadoop  for the operation is(ms) : " + timeTaken);
            System.exit(0);
        }

        else
        {
            System.out.println("Time taken by Hadoop  for the operation is(ms) :" + timeTaken);
            System.exit(1);
        }


    }

    /*Mapper for the Hadoop Sort */
    public static class MapperForSorting extends Mapper<Object, Text, Text, Text>{

        private Text keys = new Text();
        private Text values = new Text();

        public void map (Object key, Text value, Context context)throws IOException, InterruptedException{

            String keyText = (value.toString()).substring(1,10);
            String valueText  = (value.toString()).substring(10);
            keys.set(keyText);
            values.set(valueText);
            context.write(keys,values);
        }
    }

    /*Reducer for the Hadoop Sort*/
    public static class ReducerForSorting extends Reducer<Text, Text, Text, Text>{

        private Text sortedKey = new Text();
        private Text ValueForKey = new Text();

        public void reduce (Text key, Iterable<Text> values, Context context)throws IOException, InterruptedException{

            sortedKey = key;
            for (Text val : values){
                ValueForKey = val;
            }
            context.write(sortedKey,ValueForKey);
        }

    }

}
