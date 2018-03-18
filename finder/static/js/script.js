// LOAD DATA
if (
    sessionStorage.groups_data === undefined ||
    sessionStorage.teachers_data === undefined ||
    sessionStorage.subjects_data === undefined ||
    sessionStorage.hours_data === undefined ||
    sessionStorage.classrooms_data === undefined ||
    sessionStorage.days_data === undefined
){
    $.holdReady(true);

    $.when(
        $.getJSON('/api/timetable/groups'),
        $.getJSON('/api/timetable/teachers'),
        $.getJSON('/api/timetable/subjects'),
        $.getJSON('/api/timetable/hours'),
        $.getJSON('/api/timetable/classrooms'),
        $.getJSON('/api/timetable/weekdays')
    ).then(function (groups, teachers, subjects, hours, classrooms, week_days) {
        sessionStorage.groups_data = JSON.stringify(groups[0]);
        sessionStorage.teachers_data = JSON.stringify(teachers[0]);
        sessionStorage.subjects_data = JSON.stringify(subjects[0]);
        sessionStorage.hours_data = JSON.stringify(hours[0]);
        sessionStorage.classrooms_data = JSON.stringify(classrooms[0]);
        sessionStorage.days_data = JSON.stringify(week_days[0]);

        $.holdReady(false);
    });
}

$(document).ready(function(){
    $("#filter_select_type").change(function(){
        var filter_type = $(this).val();
        $("#filter_values").attr("list", filter_type);
        $("#filter_values").val("");
    });

    $("#filter_add_criteria").click(function(){
        var filter_type = $("#filter_select_type").val();
        var filter_type_name = $("#filter_select_type option:selected").text();
        var filter_value = $("#filter_values").val();

        if (!filter_type || !filter_value){
            show_error("Popraw wprowadzone dane!");
        }
        else{
            hide_error();

            var new_rule = `
                        <div class="filter-item">
                            <div class="filter-item-header">
                                <span class="filter-item-type">${filter_type_name}</span>
                                <span class="filter-item-delete">
                                    <button class="btn btn-xs btn-danger" type="button">
                                        <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                                    </button>
                                </span>
                            </div>
                            <div class="filter-item-value">
                                    ${filter_value}
                            </div>
                        </div>
            `;
            $("#filter_criterias").append(new_rule);
        }
    });





var rules_basic = {
   "condition":"AND",
   "rules":[
      {
         "id":"teacher",
         "field":"teacher",
         "type":"string",
         "input":"text",
         "operator":"equal",
         "value":"A.Bednarz"
      },
      {
         "condition":"AND",
         "rules":[
            {
               "id":"group",
               "field":"group",
               "type":"string",
               "input":"text",
               "operator":"equal",
               "value":"11A1"
            },
            {
               "id":"group",
               "field":"group",
               "type":"string",
               "input":"text",
               "operator":"equal",
               "value":"11A2"
            },
            {
               "id":"group",
               "field":"group",
               "type":"string",
               "input":"text",
               "operator":"equal",
               "value":"11A3"
            }
         ]
      },
      {
         "condition":"AND",
         "rules":[
            {
               "id":"classroom",
               "field":"classroom",
               "type":"string",
               "input":"text",
               "operator":"equal",
               "value":"A123"
            }
         ]
      }
   ],
   "valid":true
};


// Fix for Selectize
$('#builder').on('afterCreateRuleInput.queryBuilder', function(e, rule) {
  if (rule.filter.plugin == 'selectize') {
    rule.$el.find('.rule-value-container').css('min-width', '200px')
      .find('.selectize-control').removeClass('form-control');
  }
});





$('#builder').queryBuilder({
    lang_code: "pl",
    filters: [
        {
            id: 'group',
            label: 'Grupa',
            type: 'string',
            plugin: 'selectize',
            plugin_config: {
                valueField: 'id',
                labelField: 'name',
                searchField: 'name',
                sortField: 'name',
                create: true,
                maxItems: 1,
                onInitialize: function() {
                    var that = this;

                    JSON.parse(sessionStorage.groups_data).forEach(function(item) {
                            var tmp = {};
                            tmp['id'] = item;
                            tmp['name'] = item;
                            that.addOption(tmp);
                        });
                }
            },
            valueSetter: function(rule, value) {
                rule.$el.find('.rule-value-container input')[0].selectize.setValue(value);
            },
            operators: ['equal', 'not_equal', 'in', 'not_in']
        },
        {
            id: 'teacher',
            label: 'Wykładowca',
            type: 'string',
            plugin: 'selectize',
            plugin_config: {
                valueField: 'id',
                labelField: 'name',
                searchField: 'name',
                sortField: 'name',
                create: true,
                maxItems: 1,
                onInitialize: function() {
                    var that = this;

                    JSON.parse(sessionStorage.teachers_data).forEach(function(item) {
                        var tmp = {};
                        tmp['id'] = item;
                        tmp['name'] = item;
                        that.addOption(tmp);
                    });

                }
            },
            valueSetter: function(rule, value) {
                rule.$el.find('.rule-value-container input')[0].selectize.setValue(value);
            },
            operators: ['equal', 'not_equal', 'in', 'not_in']
        },
        {
            id: 'classroom',
            label: 'Sala',
            type: 'string',
            plugin: 'selectize',
            plugin_config: {
                valueField: 'id',
                labelField: 'name',
                searchField: 'name',
                sortField: 'name',
                create: true,
                maxItems: 1,
                onInitialize: function() {
                    var that = this;

                    JSON.parse(sessionStorage.classrooms_data).forEach(function(item) {
                        var tmp = {};
                        tmp['id'] = item;
                        tmp['name'] = item;
                        that.addOption(tmp);
                    });

                }
            },
            valueSetter: function(rule, value) {
                rule.$el.find('.rule-value-container input')[0].selectize.setValue(value);
            },
            operators: ['equal', 'not_equal']
        },
        {
            id: 'hour',
            label: 'Godzina',
            type: 'string',
            plugin: 'selectize',
            plugin_config: {
                valueField: 'id',
                labelField: 'name',
                searchField: 'name',
                create: true,
                maxItems: 1,
                onInitialize: function() {
                    var that = this;

                    JSON.parse(sessionStorage.hours_data).forEach(function(item) {
                        var tmp = {};
                        tmp['id'] = item;
                        tmp['name'] = item;
                        that.addOption(tmp);
                    });
                }
            },
            valueSetter: function(rule, value) {
                rule.$el.find('.rule-value-container input')[0].selectize.setValue(value);
            },
            operators: ['equal', 'not_equal']
        },
        {
            id: 'subject',
            label: 'Przedmiot',
            type: 'string',
            plugin: 'selectize',
            plugin_config: {
                valueField: 'id',
                labelField: 'name',
                searchField: 'name',
                create: true,
                maxItems: 1,
                onInitialize: function() {
                    var that = this;

                    JSON.parse(sessionStorage.subjects_data).forEach(function(item) {
                        var tmp = {};
                        tmp['id'] = item;
                        tmp['name'] = item;
                        that.addOption(tmp);
                    });
                }
            },
            valueSetter: function(rule, value) {
                rule.$el.find('.rule-value-container input')[0].selectize.setValue(value);
            },
            operators: ['equal', 'not_equal', 'in', 'not_in']
        },
        {
            id: 'day',
            label: 'Dzień',
            type: 'integer',
            plugin: 'selectize',
            plugin_config: {
                valueField: 'id',
                labelField: 'name',
                searchField: 'name',
                create: true,
                maxItems: 1,
                onInitialize: function() {
                    var that = this;

                    var json = JSON.parse(sessionStorage.days_data);

                    $.each(json, function(key, val) {
                        var tmp = {};
                        tmp['id'] = key;
                        tmp['name'] = val;
                        that.addOption(tmp);
                    });
                }
            },
            valueSetter: function(rule, value) {
                rule.$el.find('.rule-value-container input')[0].selectize.setValue(value);
            },
            operators: ['equal', 'not_equal', 'in', 'not_in']
        }
    ],
    rules: rules_basic
});

$("#send_query").click(function() {
    var filter_query = $('#builder').queryBuilder('getMongo');
    console.log(JSON.stringify(filter_query));
    $("#week_view").load("/filter?filter=" + JSON.stringify(filter_query), function() {});
});

$("#normal").click(function() {
console.log($('#builder').queryBuilder('getRules'));

});

    function show_error(message){
        console.log(message);
        $("#filter_error").css("visibility", "visible")
        $("#filter_error").text(message);
    }

    function hide_error(){
        $("#filter_error").css("visibility", "hidden")
        $("#filter_error").text("");
    }
});
