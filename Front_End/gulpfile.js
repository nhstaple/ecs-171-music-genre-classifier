//convert jsx to js file
//created by Cameron FitzPatrick, 2019
var gulp = require('gulp');
var babel = require('gulp-babel');
gulp.task("babel", function(){
    return gulp.src("src/*.jsx").
        pipe(babel({
            plugins: ['transform-react-jsx']
        })).
        pipe(gulp.dest("src"));
});
