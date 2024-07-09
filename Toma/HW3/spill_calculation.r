#!/usr/bin/env Rscript

#Reading csv file
args <- commandArgs(trailingOnly=TRUE)
data <- read.csv(args[1])

#Converting spill units to Gallons
retval <- subset(data, Units == 'Pounds')
retval$Quantity <- retval$Quantity/8
retval2 <- subset(data, Units == 'Gallons')

#Creating new dataframe
emp.data <- data.frame(
        file_name = c(args[1]),
        number_of_spills = c(nrow(data)),
        quantity_in_gallons = c(sum(retval$Quantity)+ sum(retval2$Quantity))
)
print(emp.data)
