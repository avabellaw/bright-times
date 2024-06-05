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

    $("#submit-btn").on("click", (function(event){
        let start_date = document.getElementById("id_start_date_time").value;
        let end_date = document.getElementById("id_end_date_time").value;
        let ticket_end_date = document.getElementById("id_ticket_end_date_time").value;

        if(start_date == "" || end_date === "" || ticket_end_date === ""){
            event.preventDefault();
            let fields = [];
            if(start_date === ""){
                fields.push("Event start date");
            }
            if(end_date == ""){
                fields.push("Event end date");
            }
            if(ticket_end_date == ""){
                fields.push("ticket end date");
            }

            let finalMsg = `Please fill out the fields: ${fields.join(", ")}`

            alert(finalMsg);
            
        }
    }));
});