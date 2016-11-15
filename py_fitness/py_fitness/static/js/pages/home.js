Vue.config.delimiters = ["[[","]]"];

var App = new Vue({
    el: '#app',
    data: {
        'apptitle': 'PY Fitness Dashboard',
        'workouts': []
    },
    methods: {
        $w: function (index, attr) {
            return this.workouts[index][attr];
        },
        addWorkout: function () {
            var newWorkout = {
                date: this.date.trim(),
                weight: this.weight.trim(),
                duration: this.duration.trim(),
                mood: this.mood.trim(),
                location: this.location.trim(),
                notes: this.notes.trim()
            };

            this.$http.post('http://127.0.0.1:8000/api/workouts/', newWorkout);
        },
        removeWorkout: function (index) {
            var date = this.$w(index, 'date')
            var workoutUrl = date.getFullYear().toString().concat('/', date.getMonth().toString(), '/', date.getDay().toString(), '/', this.$w(index, 'id').toString());
            this.$http.delete('http://127.0.0.1:8000/api/workouts/'.concat(workoutUrl));
            this.workouts.splice(index, 1);
        }
    },
    ready: function() {
        this.$http.get('http://127.0.0.1:8000/api/workouts/').then(function (response) {
            this.workouts = response.data;
        },
        function (response) {
            console.log(response);
        });
    }
});
