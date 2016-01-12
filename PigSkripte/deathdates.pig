SET default_parallel $reducerNum ; 
SET job.name '$jobName ON $inputData STORED TO $outputData' ; 


-- load input data 
inputData = LOAD '$inputData' USING PigStorage('\n') AS (line:chararray);

result = FILTER inputData by (line matches '[^\t]*\t{1}.*\t{1,}"$date.*');

-- store results into output
STORE result INTO '$outputData' USING PigStorage('\n');
