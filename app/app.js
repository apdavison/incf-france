angular.module('YourApp', ['ngMaterial', 'ngResource', 'ui.router', 'ng-showdown', 'angularFileUpload'])

// .config(function($compileProvider) {
//   // this seems to be needed to access `this.project` inside `ProjectController`
//   // see https://docs.angularjs.org/guide/migration#commit-bcd0d4
//   $compileProvider.preAssignBindingsEnabled(true);
// })

.config(function($stateProvider) {
  $stateProvider
    .state('home', {
      url: '',
      component: 'home'
    })
    .state('about', {
      url: '/about',
      component: 'about'
    })
    .state('people', {
      url: '/people',
      component: 'people',
      resolve: {
        people: function(People) {
          return People.query();
        }
      }
    })
    .state('person', {
      url: '/people/{id}',
      component: 'person',
      resolve: {
        person: function(People, Projects, $transition$) {
          console.log("id: " + $transition$.params().id);
          return People.get({id: $transition$.params().id},
            function(person) {
              person.projectObjs = [];
              for (let project of person.projects) {
                person.projectObjs.push(Projects.get({id: project.label}));
              }
              return person;
            }
          );
        }
      }
    })
    .state('projects', {
      url: '/projects',
      component: 'projects',
      resolve: {
        projects: function(Projects) {
          return Projects.query();
        }
      }
    })
    .state('new-project', {
      url: '/projects/new',
      component: 'project',
      resolve: {
        project: function(Projects) {
          var new_proj = new Projects();


        }
      }
    })
    .state('project', {
      url: '/projects/{id}',
      component: 'project',
      resolve: {
        project: function(Projects, People, $transition$) {
          console.log("id: " + $transition$.params().id);
          return Projects.get({id: $transition$.params().id},
            function(project) {
              project.contributorObjs = [];
              for (let contributor of project.contributors) {
                project.contributorObjs.push(People.get({id: contributor.label}));
              }
              console.log(project.contributorObjs);
              return project;
            },
            function(err) {
              console.log(err);
            }
          );
        },
        people: function(People) {
          return People.query();
        }
      }
    })
    .state('workshops', {
      url: '/workshops/geant2019',
      component: 'workshops'
    })
    ;
})
.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('purple')
    .accentPalette('teal', {
      'default': '500'
    });
})
.run(function($rootScope) {
  $rootScope.$on('$stateChangeStart',function(event, toState, toParams, fromState, fromParams){
      console.log('$stateChangeStart to '+toState.name+' - fired when the transition begins. toState,toParams : \n',toState, toParams);
    });
    $rootScope.$on('$stateChangeError',function(event, toState, toParams, fromState, fromParams, error){
      console.log('$stateChangeError - fired when an error occurs during transition.');
      console.log(arguments);
    });
    $rootScope.$on('$stateChangeSuccess',function(event, toState, toParams, fromState, fromParams){
      console.log('$stateChangeSuccess to '+toState.name+' - fired once the state transition is complete.');
    });
    $rootScope.$on('$viewContentLoading',function(event, viewConfig){
       console.log('$viewContentLoading - view begins loading - dom not rendered',viewConfig);
    });

    /* $rootScope.$on('$viewContentLoaded',function(event){
         // runs on individual scopes, so putting it in "run" doesn't work.
         console.log('$viewContentLoaded - fired after dom rendered',event);
       }); */

    $rootScope.$on('$stateNotFound',function(event, unfoundState, fromState, fromParams){
      console.log('$stateNotFound '+unfoundState.to+'  - fired when a state cannot be found by its name.');
      console.log(unfoundState, fromState, fromParams);
    });
})
;
