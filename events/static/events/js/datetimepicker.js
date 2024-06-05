$(function(){
    /* Have to initalize them seperately to treat them as seperate
       When adding minDate and maxDate etc */
    $("#id_start_date_time").datetimepicker({
        inline:true,
        step:15,
        format:'Y-m-d H:i',
    });

    $("#id_end_date_time").datetimepicker({
        inline:true,
        step:15,
        format:'Y-m-d H:i',
    });

    $("#id_ticket_end_date_time").datetimepicker({
        inline:true,
        step:15,
        format:'Y-m-d H:i',
    });

    $("#id_start_date_time").on('change', function(){
        let datetime = new Date(document.getElementById("id_start_date_time").value);
        $("#id_end_date_time").datetimepicker({
            minDate: datetime,
            minTime: datetime,
        });

        $("#id_ticket_end_date_time").datetimepicker({
            maxDate: datetime,
            maxTime: datetime
        });
    });
});