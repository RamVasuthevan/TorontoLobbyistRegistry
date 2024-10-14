open TorontoLobbyistRegistry.log
| lines
| where { |line| 
    let columns = $line | split row " " ;
    let process_name = if ($columns | length) > 4 {
        ($columns | get 4 | split row "[" | get 0 | default "")
    } else {
        ""
    };
    $process_name == "bash"
}
| each { |line| 
    let parts = $line | split row " "
    let datetime = $parts.0 + " " + $parts.1 + " " + $parts.2
    let machine_name = $parts | get 3
    let process_name = $parts | get 4 | split row "[" | get 0
    let process_id = $parts | get 4 | split row "[" | get 1 | str trim --char ":" | str trim --char "]"
    let log_level = $parts | get 5 | str trim --char ":"
    let message = $parts | skip 6 | str join " "

    # Check if a valid IP address exists using a regular expression
    let is_valid_ip = if ($message | parse --regex '\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b' | length) > 0 {
        "true"
    } else {
        "false"
    }

    let ip_address = if $is_valid_ip == "true" {
        $parts.10
    } else {
        ""
    }

    let http_method = if $log_level == "INFO" and $is_valid_ip == "true" {
       $parts.12 | str trim --char "\""
    } else {
        ""
    }

    let url = if $log_level == "INFO" and $is_valid_ip == "true" {
        $parts.13 
    } else {
        ""
    }

    let http_protocol = if $log_level == "INFO" and $is_valid_ip == "true" {
        $parts.14
    } else {
        ""
    }

    let http_status = if $log_level == "INFO" and $is_valid_ip == "true" {
        $parts | skip 15 | str join " "
    } else {
        ""
    }


    { datetime: $datetime, process_name: $process_name, process_id: $process_id, log_level: $log_level, ip_address: $ip_address, http_method: $http_method, http_protocol: $http_protocol, http_status: $http_status }
}
| where log_level == "INFO"