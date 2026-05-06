'use strict';

angular.module('YourApp')

.component('home', {
  templateUrl: 'static/home.tpl.html'
})

.component('about', {
  templateUrl: 'static/about.tpl.html'
})

.component('people', {
  bindings: { people: '<' },
  templateUrl: 'static/people.tpl.html'
})

.component('person', {
  bindings: { person: '<' },
  controller: 'PersonController',
  templateUrl: 'static/person.tpl.html'
})

.component('projects', {
  bindings: { projects: '<' },
  controller: 'ProjectController',
  templateUrl: 'static/projects.tpl.html'
})

.component('project', {
  bindings: {
    project: '<',
    people: '<'
  },
  controller: 'ProjectController',
  templateUrl: 'static/project.tpl.html'
})

.component('workshops', {
  templateUrl: 'static/geant2019.tpl.html'
})

;
