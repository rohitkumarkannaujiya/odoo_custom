/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoTable extends Component {
    static props = {
        list: {
            type: Array,
            element: {
                type: Object,
                shape: {
                    id: Number,
                    name: String,
                    isCompleted: Boolean,
                }
            }
        },
        onDelete: { type: Function },
        completeTodo: { type: Function },
        updateTodo: { type: Function },
        searchTodo: { type: Function },
    }

    static template = 'todotable'

    remove(index) {
        this.props.onDelete(index);
    }
    complete(index) {
        this.props.completeTodo(index);
    }
    update(index) {
        this.editt = true
        this.props.updateTodo(index);
    }
    search(e) {
        let val = e.target.value;
        this.props.searchTodo(val);
    }
}