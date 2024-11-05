/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoTable } from "./todotable";
import { Header } from "./header";
import { TodoMini } from "./todomini";

export class Todo extends Component {
    todolist = [{
        id: 1,
        name: "task1",
        isCompleted: true
    }, {
        id: 2,
        name: "task2",
        isCompleted: false
    }, {
        id: 3,
        name: "task3",
        isCompleted: true
    }, {
        id: 4,
        name: "tas4",
        isCompleted: false
    }, {
        id: 5,
        name: "task5",
        isCompleted: false
    },
    ]
    static template = "playground";
    static components = { TodoTable,Header, TodoMini }
    edit = {mode : false , id : null};
    date = new Date().toDateString()

    setup() {
        this.state = useState({
            nextId : Math.max(...this.todolist.map(t => t.id)) +1,
            list : [...this.todolist],
            name : '',
            todolists : [],  // for multiple mini todolists.
        })
    }

// Function to Add or update todo
    addTodo(){
        let newTodoTitle = this.state.name;
        if(newTodoTitle.length <1)
        return
        if(this.edit.mode){
            this.state.list[this.edit.id].name = newTodoTitle
            this.edit.mode = false
            this.edit.id= null
        }else{
            this.state.list.push({
                id : this.state.nextId++ , 
                name : newTodoTitle,
                isCompleted : false
            })
        }
        this.state.name = '';
    }
    // function to delete todo
    removeTodo(index){
        this.state.list.splice(index,1);
    }
    // function to mark to as complete
    completeTodo(index){
        this.state.list[index].isCompleted = true;
    }
    // function for setting todo in update mode.
    editTodo(id){
        this.edit.id = id
        this.edit.mode = true
        this.state.name = this.state.list[id].name
    }
    searchTodo(val){
        if(val.length <3 && this.state.list.length != this.todolist.length){
            this.state.list = [...this.todolist]
        }else{
            this.state.list = this.state.list.filter( t => t.name.includes(val))
        }
    }

    /**
     * Function for todomini
     */
    addTodolist(){
        this.state.todolists.push(TodoMini)
    }
}