// Generated on 2016-02-09 using generator-angular 0.15.1
'use strict';

var gulp = require('gulp');
var $ = require('gulp-load-plugins')();
var lazypipe = require('lazypipe');
var rimraf = require('rimraf');
var wiredep = require('wiredep').stream;
var runSequence = require('run-sequence');
var _ = require('lodash');

var yeoman = {
  app: 'app',
  dist: 'dist'
};

var paths = {
  scripts: [yeoman.app + '/scripts/**/*.js'],
  styles: [yeoman.app + '/styles/**/*.css'],
  views: {
    main: [yeoman.app + '/index.html', 'app/vendor_scripts.html', 'app/login.html', 'app/embed.html', 'app/public.html', 'app/app_layout.html', 'app/signed_out_layout.html'],
    files: [yeoman.app + '/views/**/*.html']
  }
};

////////////////////////
// Reusable pipelines //
////////////////////////

var lintScripts = lazypipe()
  .pipe($.jshint, '.jshintrc')
  .pipe($.jshint.reporter, 'jshint-stylish');

var styles = lazypipe()
  .pipe($.autoprefixer, 'last 1 version')
  .pipe(gulp.dest, '.tmp/styles');

///////////
// Tasks //
///////////

gulp.task('styles', function () {
  return gulp.src(paths.styles)
    .pipe(styles())
    .pipe($.livereload());
});

gulp.task('lint:scripts', function () {
  return gulp.src(paths.scripts)
    .pipe(lintScripts());
});

gulp.task('clean:tmp', function (cb) {
  rimraf('./.tmp', cb);
});

// inject bower components
gulp.task('bower', function () {
  return gulp.src(paths.views.main)
    .pipe(wiredep({
      directory: yeoman.app + '/bower_components',
      ignorePath: '..'
    }))
  .pipe(gulp.dest(yeoman.app + '/views'));
});

///////////
// Build //
///////////

gulp.task('clean:dist', function (cb) {
  rimraf('./dist', cb);
});

gulp.task('client:build', ['html', 'styles'], function () {
  var jsFilter = $.filter('**/*.js');
  var cssFilter = $.filter('**/*.css');

  return gulp.src(paths.views.main)
    .pipe($.useref({searchPath: [yeoman.app, '.tmp']}))
    .pipe(jsFilter)
    .pipe($.ngAnnotate())
    .pipe($.uglify())
    .pipe(jsFilter.restore())
    .pipe($.print())
    .pipe(cssFilter)
    .pipe($.minifyCss({cache: true}))
    .pipe(cssFilter.restore())
    .pipe(new $.revAll({dontRenameFile: ['.html'], dontUpdateReference: ['vendor_scripts.html', 'app_layout.html', 'signed_out_layout.html']}).revision())
    .pipe(gulp.dest(yeoman.dist));
});

gulp.task('html', function () {
  return gulp.src(yeoman.app + '/views/**/*')
    .pipe(gulp.dest(yeoman.dist + '/views'))
    .pipe($.livereload());
});

gulp.task('images', function () {
  return gulp.src(yeoman.app + '/images/**/*')
    .pipe($.cache($.imagemin({
        optimizationLevel: 5,
        progressive: true,
        interlaced: true
    })))
    .pipe(gulp.dest(yeoman.dist + '/images'));
});

gulp.task('copy:extras', function () {
  return gulp.src([yeoman.app + '/*/.*', 'app/google_login.png', 'favicon.ico', 'robots.txt'], { dot: true })
    .pipe(gulp.dest(yeoman.dist));
});

gulp.task('copy:fonts', function () {
  return gulp.src([yeoman.app + '/fonts/**/*', 'app/bower_components/font-awesome/fonts/*', 'app/bower_components/material-design-iconic-font/dist/fonts/*'])
    .pipe(gulp.dest(yeoman.dist + '/fonts'));
});

gulp.task('build', ['clean:dist'], function () {
  runSequence(['images', 'copy:extras', 'copy:fonts', 'client:build']);
});

var scriptsjs = function(p){
  var jsFilter = $.filter('**/*.js');
  return gulp.src(p)
    .pipe($.useref({searchPath: [yeoman.app, '.tmp']}))
    .pipe(jsFilter)
    .pipe($.ngAnnotate())
    .pipe(jsFilter.restore())
    .pipe($.print())
    .pipe(new $.revAll({dontRenameFile: ['.html'], dontUpdateReference: ['vendor_scripts.html', 'app_layout.html', 'signed_out_layout.html']}).revision())
    .pipe(gulp.dest(yeoman.dist))
    .pipe($.livereload());
};

gulp.task('dev:pre', function () {
  scriptsjs(paths.views.main);
});

gulp.task('dev:pos', function () {
  scriptsjs(_.difference(paths.views.main, ['vendor_scripts.html']));
});

gulp.task('dev', ['clean:dist'], function () {
  runSequence(
    ['images', 'copy:extras', 'copy:fonts'],
    ['html', 'styles'],
    'dev:pre',
    function(){
      $.livereload.listen();
      gulp.watch([paths.styles], ['styles']);
      gulp.watch([paths.views.files], ['html']);
      gulp.watch([paths.scripts], ['dev:pos']);
    }
  );
});

gulp.task('default', ['build']);
