<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full">
                
                <p><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <p class="text-xs text-gray-500">{{ user.friends_count }} friends</p>
                    <p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
                </div>

               
            </div>
        </div>

        <div class="main-center col-span-2 space-y-4">
            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg grid "
                v-if="friendshipRequests.length"
            >
                <h2 class="text-xl mb-6">Freindship Request</h2>
                <div 
                    class="p-4 text-center bg-gray-100 rounded-lg bg-white border border-gray-200 rounded-lg grid mb-4"
                    v-for="friendRequest in friendshipRequests"
                    v-bind:key="friendRequest.id"
                >
                    <img src="https://i.pravatar.cc/100?img=70" class="mb-6 mx-auto rounded-full">
                
                    <p>
                        <strong>
                            <RouterLink :to="{name: 'profile', params:{'id': friendRequest.created_by.id}}"> {{ friendRequest.created_by.name }} </RouterLink>
                        </strong>
                    </p>

                    <div class="mt-6 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">{{ user.friends_count }} friends</p>
                        <p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
                    </div>

                    <div class="mt-6 space-x-4">
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg" @click="handleRequest('accepted', friendRequest.created_by.id)" >Accept</button>
                        <button class="inline-block py-4 px-6 bg-red-600 text-white rounded-lg" @click="handleRequest('rejected', friendRequest.created_by.id)" >Reject</button>
                    </div>
                </div>
                <hr>
                
            </div>

             <div 
                class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-3 gap-4"
                v-if="friends.length"
            >
                <div 
                    class="p-4 text-center bg-gray-100 rounded-lg"
                    v-for="user in friends"
                    v-bind:key="user.id"
                >
                    <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full">
                
                    <p>
                        <strong>
                            <RouterLink :to="{name: 'profile', params:{'id': user.id}}"> {{ user.name }} </RouterLink>
                        </strong>
                    </p>

                    <div class="mt-6 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">{{ user.friends_count }} friends</p>
                        <p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
                    </div>
                </div>

                
            </div>
        </div>



        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />

            <Trends />
        </div>
    </div>
</template>

<script>
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import { useUserStore } from '@/stores/user'
import axios from 'axios'


export default {
    name: 'FriendsView',

    setup() {
        const userStore = useUserStore()
        
        return {
            userStore
        }
    },

    components: {
        PeopleYouMayKnow,
        Trends,
        
    },

    data() {
        return {
            user: {},
            friends: {},
            friendshipRequests: {}
        }
    },

    mounted () {
       this.getFriends()
    },

   

    methods: {
        getFriends() {
            axios
                .get(`/api/friends/${this.$route.params.id}/`)
                .then( response => {
                    console.log(response.data)

                    this.friendshipRequests = response.data.requests 
                    this.user = response.data.user
                    this.friends = response.data.friends
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        handleRequest(status, pk) {
            console.log('handleRequest', status, `${this.$route.params.id}`)

            axios
                .post(`/api/friends/${pk}/${status}/`)
                .then(response => {
                    console.log('data', response.data)

                   
                })
                .catch(error => {
                    console.log('error', error)
                })
        }
    }
}
</script>