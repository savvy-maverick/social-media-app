<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        

        <div class="main-center col-span-3 space-y-4">
         

           
            
            

            <div class="p-4 bg-white border border-gray-200 rounded-lg"
              v-if="post.id"
            >
                <FeedItem v-bind:post="post"/>  
            </div>

            <div 
                class="bg-white border border-gray-200 rounded-lg"
                v-for="comment in post.comments"
                v-bind:key="comment.id"
            >
            
               
            </div>

               <div class="bg-white border border-gray-200 rounded-lg">
              <form v-on:submit.prevent="submitForm" method="post" >
                <div class="p-4">  
                    <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What do you think?"></textarea>
                </div>

                <div class="p-4 border-t border-gray-100">
                    

                    <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Comment</button>
                </div>
              </form>
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />

            <Trends />
        </div>
    </div>
</template>

<script>
import FeedItem from '../components/FeedItem.vue'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import { useUserStore } from '@/stores/user'
import axios from 'axios'

export default {
    name: 'PostView',
    setup() {
            const userStore = useUserStore()

            return {
                userStore
            }
        },
    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem,
    },

    data() {
        return {
            post: {
                id: null,
                comments: []
            },
            body: ''

            
        }
    },

    mounted () {
        this.getPost()
    },

    methods: {
        getPost() {
            axios
                .get(`/api/posts/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data)
                    this.post = response.data.post
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        submitForm() {
            console.log('submitform', this.body)

            axios
                .post(`/api/posts/${this.$route.params.id}/comment/`, {
                    'body': this.body
                })
                .then( response => {
                    console.log('data:', response.data)
                    
                    this.post.comments.unshift(response.data)
                    this.body = ''
                })
                .catch(error => {
                    console.log('error', error)
                })
        }
    }
}
</script>