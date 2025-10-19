#!/bin/bash

# A shell script to download AMFI NAV data and extract specific fields.

# changed url of the assignment as it is updated 
readonly URL="https://portal.amfiindia.com/spages/NAVAll.txt"
OUTPUT_FILE="nav_results.tsv"

main() {
    echo "Starting NAV data processing"
    # Download and process the data, then save to TSV file
    echo "Scheme Name       Net Asset Value" > "$OUTPUT_FILE"
    curl -s "$URL" | awk -F';' 'NR > 1 && $4 != "" {print $4 "\t" $5}' >> "$OUTPUT_FILE"
    
    # Count the number of records saved
    record_count=$(( $(wc -l < "$OUTPUT_FILE") - 1 ))
    echo "Done. $record_count records saved to $OUTPUT_FILE"
}

# calling the main function to start the script
main "$@"

