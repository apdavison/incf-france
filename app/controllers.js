'use strict';

angular.module('YourApp')

.controller("PersonController", function($http, FileUploader){
    var vm = this;
    vm.editing = false;

    var error = function(response) {
        console.log(response);
    };

    var orcid_login = null;
    $http.get("/directory/profile/", {}).then(
        function(response) {
            orcid_login = response.data["orcid"];
            console.log("Logged in with ORCID " + orcid_login);
        },
        error);

    vm.canEdit = function() {
        return vm.person.orcid === orcid_login
    }

    vm.editPerson = function() {
        vm.editing = true;
    }

    vm.saveChanges = function() {
        vm.editing = false;
        vm.person.$update({'id': vm.person.label});
    }

    vm.getUploader = function() {
        vm.uploader = new FileUploader({"url": "/api/v0/people/" + vm.person.label + "/photo"});
        return vm.uploader
    }
})

.controller("ProjectController", function($http, FileUploader, Licences){
    console.log("Project:");
    var vm = this;
    vm.editing = false;
    vm.addingContributor = false;
    vm.licences = [];
    //vm.selectedLicence = "";

    var error = function(response) {
        console.log(response);
    };

    var orcid_login = null;
    $http.get("/directory/profile/", {}).then(
        function(response) {
            orcid_login = response.data["orcid"];
            console.log("Logged in with ORCID " + orcid_login);
        },
        error);

    vm.canEdit = function() {
        var contributor_orcids = [];
        for (let contributor of vm.project.contributors) {
            if (contributor.orcid) {
                contributor_orcids.push(contributor.orcid);
            }
        }
        if (contributor_orcids.indexOf(orcid_login) >= 0) {
            return true;  //orcid_login is in list of contributors' orcids
        } else {
            return false;
        }
    }

    vm.canAddProject = function() {
        return Boolean(orcid_login); //is logged in
    }

    vm.editProject = function() {
        vm.editing = true;
        if (vm.licences.length == 0) {
            Licences.get(
                function(response) {
                    vm.licences = response.licenses.map(item => item.name);
                    console.log(vm.licences);
                }
            );
        }
    }

    vm.selectContributor = function() {
        vm.newContributor = null;
        vm.addingContributor = true;
        console.log("Adding contributor");
    }

    vm.saveContributor = function() {
        vm.project.contributorObjs.push(vm.newContributor);
        vm.project.contributors.push({
            label: vm.newContributor.label
        });
        console.log(vm.project.contributorObjs);
        console.log(vm.project.contributors);
        vm.addingContributor = false;
        vm.newContributor = null;
    }

    vm.licenceSearch = function(query) {
        var results = query ? vm.licences.filter(item => item.indexOf(query) === 0) : vm.licences;
        return results;
    }

    // vm.setLicence = function(item) {
    //     if (item) {
    //         vm.project.licence = item.name;
    //     }
    // }

    vm.cancel = function() {
        vm.editing = false;
        vm.addingContributor = false;
        vm.newContributor = null;
    }

    vm.cancelAddingContributor = function() {
        vm.addingContributor = false;
        vm.newContributor = null;
    }

    vm.saveChanges = function() {
        vm.editing = false;
        vm.project.$update({'id': vm.project.label});
    }

    vm.getUploader = function() {
        vm.uploader = new FileUploader({"url": "/api/v0/projects/" + vm.project.label + "/logo"});
        return vm.uploader
    }

})

.controller("ProfileController", function($http) {
    var vm = this;

    var error = function(response) {
        console.log("Not logged in");
    };

    vm.orcid = null;
    $http.get("/directory/profile/", {}).then(
        function(response) {
            vm.orcid = response.data["orcid"];
        },
        error);
});