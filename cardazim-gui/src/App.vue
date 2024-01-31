<script>
import Card from "./components/Card.vue"

export default {
    data() {
        return {
            creators: [],
            selected_creator: "",
            cards: []
        };
    },

    components: {
        Card
    },

    methods: {
        async refresh_creators() {
            try {
                const response = await fetch("http://127.0.0.1:5000/creators");
                this.creators = await response.json();
            }
            catch (err) {
                console.log(err);
            }
        },
        async fetch_card_metadata(creator, name) {
            const response = await fetch("http://127.0.0.1:5000/creators/"
                + creator + "/cards/" + name + "/");
            return await response.json();
        },
        async refresh_cards() {
            try {
                const response =
                    await fetch("http://127.0.0.1:5000/creators/"
                        + this.selected_creator + "/cards/");
                let card_names = await response.json();
                this.cards = []
                card_names.forEach(async name => {
                    this.cards.push(
                        await this.fetch_card_metadata(this.selected_creator, name)
                    );
                });
            }
            catch (err) {
                console.log(err);
            }
        },
    }
}
</script>

<template>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
            integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    </head>

    <div>
        <button @click="refresh_creators">Refresh Creators</button>
        <select v-model="selected_creator" @change="refresh_cards">
            <option v-for="creator in creators">
                {{ creator }}
            </option>
        </select>
    </div>

    <Card v-for="card in cards" :card="card" />
</template>
