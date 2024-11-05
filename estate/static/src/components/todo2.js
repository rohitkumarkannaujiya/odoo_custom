/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Todo2 extends Component{
    static template = 'todo'

    static props = {
        todo : {
            type: Object,
            shape : {id : Number, name : String , done : Boolean}
        }
    }
}