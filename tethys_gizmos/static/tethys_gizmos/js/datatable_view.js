/*****************************************************************************
 * FILE:    datatable_view.js
 * DATE:    November 2016
 * AUTHOR: Alan D. Snow
 * LICENSE: BSD 2-Clause
 *****************************************************************************/

/*****************************************************************************
 *                      LIBRARY WRAPPER
 *****************************************************************************/

var TETHYS_DATATABLE_VIEW = (function() {
	// Wrap the library in a package function
	"use strict"; // And enable strict mode for this library

	/************************************************************************
 	*                      MODULE LEVEL / GLOBAL VARIABLES
 	*************************************************************************/
 	var public_interface;				// Object returned by the module

     /************************************************************************
 	*                    PRIVATE FUNCTION DECLARATIONS
 	*************************************************************************/
 	// private methods
 	var initTableView;

 	initTableView = function(tag) {
        $(tag).DataTable();
 	};

	/************************************************************************
 	*                            TOP LEVEL CODE
 	*************************************************************************/
	/*
	 * Library object that contains public facing functions of the package.
	 */
	public_interface = {
        initTableView: initTableView,
     };

	// Initialization: jQuery function that gets called when
	// the DOM tree finishes loading
	$(function() {
        initTableView(".data_table_gizmo_view");
	});

	return public_interface;

}()); // End of package wrapper

/*****************************************************************************
 *                      Public Functions
 *****************************************************************************/

/* This statement for testing coverage purposes */
/* istanbul ignore next */
if (typeof module !== "undefined" && module.exports) {
    module.exports = { ...TETHYS_DATATABLE_VIEW} ;
}