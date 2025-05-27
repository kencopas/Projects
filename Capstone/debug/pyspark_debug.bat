@echo off
setlocal EnableDelayedExpansion

echo.
echo Environment Variables:
for %%V in (SPARK_HOME HADOOP_HOME PYSPARK_PYTHON JAVA_HOME) do echo %%V = !%%V!

echo.
echo Java Version:
java -version

echo.
echo Python Version:
python --version
echo.