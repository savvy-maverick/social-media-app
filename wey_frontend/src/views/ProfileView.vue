<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img :src="user.get_avatar" class="mb-6 rounded-full">
                
                <p><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <RouterLink :to="{name: 'friends', params: {id: userStore.user.id }}" class="text-xs text-gray-500">{{ user.friends_count }} friends</RouterLink>
                    <p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
                </div>

                <div class="mt-6" >
                    <button 
                        v-if="userStore.user.id !== user.id" 
                        class="inline-block py-2 px-6 bg-purple-600 text-xs text-white rounded-lg" 
                        @click="sendFriendshipRequest">Send friendship request
                    </button>

                    <button 
                        v-if="userStore.user.id !== user.id" 
                        class="inline-block mt-4 py-2 px-6 bg-purple-600 text-xs text-white rounded-lg" 
                        @click="sendDirectMessage">
                            Send direct message
                    </button>

                    <RouterLink to="/profile/edit"
                        v-if="userStore.user.id === user.id" 
                        class="inline-block mr-2 py-2 px-6 bg-purple-600 text-xs text-white rounded-lg" 
                        >Edit profile
                    </RouterLink>

                    <button 
                        v-if="userStore.user.id === user.id" 
                        class="inline-block py-2 px-6 bg-red-600 text-xs text-white rounded-lg" 
                        @click="logout">Logout
                    </button>
                    
                </div>
            </div>
        </div>

        <div class="main-center col-span-2 space-y-4">
            <div 
                class="bg-white border border-gray-200 rounded-lg"
                v-if="userStore.user.id === user.id"
            >
              <form v-on:submit.prevent="submitForm" method="post" >
                <div class="p-4">  
                    <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>

                    <div id="preview" v-if="url">
                        <img  :src="url" class="w-[100px] mt-3 rounded-xl"/>
                    </div>
                </div>

                <div class="p-4 border-t border-gray-100 flex justify-between">
                    

                    
                    <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                        <input type="file" ref="file" @change="onFileChange">
                        Attach image
                    </label>

                    <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                </div>
              </form>
            </div>

           
            
            

            <div class="p-4 bg-white border border-gray-200 rounded-lg"
                v-for="post in posts"
                v-bind:key="post.id"
            >
                <FeedItem v-bind:post="post"/>

            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />

            <Trends />
        </div>
    </div>
</template>

<style>
input[type='file'] {
    display: none;
}

.custom-file-upload{
    border: 1px solid #ccc;
    display: inline-block;
    padding: 6px 12px;
    cursor: pointer;
}
</style>

<script>
import { RouterLink } from 'vue-router'
import FeedItem from '../components/FeedItem.vue'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import axios from 'axios'

export default {
    name: 'FeedView',

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()


        return {
            userStore,
            toastStore
        }
    },

    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem,
    },

    data() {
        return {
            posts: [],
            body: '',
            user: {
                id: null,
            },
            url: null,
        }
    },

    mounted () {
        this.getFeed()
    },

    watch: {
      '$route.params.id': {
         handler: function() {
            console.log('kkkkkk')
            this.getFeed()
         },
         deep: true,
         immediate: true
    }
   },

    methods: {
        onFileChange(e) {
            const file = e.target.files[0];
            this.url = URL.createObjectURL(file);
        },

        sendDirectMessage() {
            console.log('senddirectmessage')

            axios
                .get(`/api/chat/${this.$route.params.id}/get-or-create/`)
                .then(response => {
                    console.log(response.data)

                    this.$router.push('/chat')
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        sendFriendshipRequest() {
            axios
                .post(`/api/friends/${this.$route.params.id}/request/`)
                .then (response => {
                    console.log(response.data)
                    if (response.data.message == 'request already sent') {
                        this.toastStore.showToast(5000, 'The request has already been sent', 'bg-red-300')
                    }
                    else{
                        this.toastStore.showToast(5000, 'The request was sent', 'bg-red-300')
                    }

                })
                .catch(error => {
                    console.log('error', error)
                })
        },


        getFeed() {
            axios
                .get(`/api/posts/profile/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data)
                    this.posts = response.data.posts
                    this.user = response.data.user
                    console.log(this.user)
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        submitForm() {
            console.log('submitform', this.body, this.$refs.file.files[0])
            let formData = new FormData()
            formData.append('image', this.$refs.file.files[0])
            formData.append('body', this.body)
            console.log('submitform', this.body)

            axios
                .post('/api/posts/create/', formData, {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                
                  })
                .then( response => {
                    console.log('data:', response.data)
                    
                    this.posts.unshift(response.data)
                    this.body = ''
                    this.$refs.file.value = null
                    this.url = null
                    this.user.posts_count += 1
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        logout() {
            console.log('Log out')

            this.userStore.removeToken()

            this.$router.push('/login')
        }
    }
}
</script>