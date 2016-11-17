var moment = require('moment-timezone');

Vue.config.delimiters = ["[[","]]"];

Vue.component('datepicker', {
template: '\
  <input class="form-control datepicker"\
        ref="input"\
        v-bind:value="value"\
        v-on:input="updateValue($event.target.value)"\
        data-date-format="yyyy-mm-dd"\
        data-date-end-date="0d"\
        placeholder="yyyy-mm-dd"\
        type="text"  />\
',
props: {
    value: {
      type: String,
      default: new Date().toISOString().slice(0, 10)
    }
},
mounted: function() {
    let self = this;
    this.$nextTick(function() {
        $(this.$el).datepicker({
            startView: 0,
            todayHighlight: true,
            todayBtn: "linked",
            autoclose: true,
            format: "yyyy-mm-dd"
        })
        .on('changeDate', function(e) {
            var date = e.format('yyyy-mm-dd');
            self.updateValue(date);
        });
    });
},
methods: {
    updateValue: function (value) {
        this.$emit('input', value);
    },
}
});

Vue.component('clockpicker', {
template: '\
  <input class="form-control clockpicker"\
        ref="input"\
        v-bind:value="value"\
        v-on:input="updateValue($event.target.value)"\
        data-autoclose="true"\
        data-align="left"\
        data-placement="bottom"\
        type="text"  />\
',
props: {
    value: {
      type: String
    }
},
mounted: function() {
    let self = this;
    this.$nextTick(function() {
        $(this.$el).clockpicker({
            autoclose: true,
            donetext: "Ok",
            twelvehour: true,
            afterDone: self.updateValue
        });
    });
},
methods: {
    updateValue: function () {
        this.$emit('input', $(this.$el)[0].value);
    },
}
});

var App = new Vue({
    el: '#app',
    data: {
        'apptitle': 'PY Fitness Dashboard',
        'workouts': [],
        'date': '',
        'time': '',
        'weight': '',
        'mood': '',
        'location': '',
        'notes': ''
    },
    methods: {
        getCookie: function(name) {
          var cookieValue = null;
          if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i=0; i<cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
              }
            }
          }
          return cookieValue;
        },
        $w: function (index, attr) {
            return this.workouts[index][attr];
        },
        twentyFourHours: function (time) {
            if (time.match(/am/gi) == null) {
              time = time.match(/(0?[1-9]|1[012])[:]([1-5][0-9]|0[0-9])/);
              hours = (parseInt(time[1]) + 12).toString();
              time = hours.concat(":",time[2]);
              return time
            } else {
              return time.match(/(0?[1-9]|1[012])[:]([1-5][0-9]|0[0-9])/)[0]
            }
        },
        addWorkout: function () {
            var csrftoken = this.getCookie('csrftoken');
            var headers = new Headers();
            headers.set('X-CSRFToken', csrftoken);

            var time = this.twentyFourHours(this.time.trim());
            var zone = moment.tz.guess()
            zone.parse()
            d = moment(this.date.trim() + " " + time, zone.name)
            var newWorkout = {
                date: d,
                weight: this.weight.trim(),
                mood: this.mood.trim(),
                location: this.location.trim(),
                notes: this.notes.trim()
            };

            this.$http.post('http://localhost:8000/api/workouts/', newWorkout, headers);
        },
        removeWorkout: function (index) {
            var date = this.$w(index, 'date')
            var workoutUrl = date.getFullYear().toString().concat('/', date.getMonth().toString(), '/', date.getDay().toString(), '/', this.$w(index, 'id').toString());
            this.$http.delete('http://localhost:8000/api/workouts/'.concat(workoutUrl));
            this.workouts.splice(index, 1);
        }
    },
    mounted: function() {
        this.$http.get('http://localhost:8000/api/workouts/').then(function (response) {
            this.workouts = response.data;
        },
        function (response) {
            console.log(response);
        });
    }
});
