'use strict';

angular.module('YourApp')

.factory(
    'People',
    function($resource, Teams) {
        return $resource('/api/v0/people/:id',
                         {id: '@id'},
                         {update: {method: 'PUT', params: {id: '@id'}}});
    }
)
.factory(
    'Teams',
    function($resource){
        return $resource('/api/v0/teams/:id',
                         {id: '@id'},
                         {update: {method: 'PUT', params: {id: '@id'}}});
    }
)
.factory(
    'Projects',
    function($resource){
        return $resource('/api/v0/projects/:id',
                         {id: '@id'},
                         {update: {method: 'PUT', params: {id: '@id'}}});
    }
)
.factory(
    'Licences',
    function($resource){
        return $resource('https://raw.githubusercontent.com/spdx/license-list-data/master/json/licenses.json');
    }
)
;