/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Todo2 } from "./todo2";

export class TodoMini extends Component{
    static template = 'todoapp'
    static components = {Todo2}

    setup() {
        this.state = useState({
            nextId : 1,
            list : [],
            name : ''
        })

        console.log(this.props);
    }


    addTodo(e){
        if(e.code=='Enter' || e.pointerId == '1'){

            let task = this.state.name;
            if(task.length > 1){
                this.state.list.push({
                    id: this.state.nextId++,
                    name: task,
                    done : false
                })
            }
            this.state.name=''
        }
    }

    completeTodo(index){
        this.state.list[index].done = true;
    }
    removeTodo(index){
        this.state.list.splice(index,1);
    }
}