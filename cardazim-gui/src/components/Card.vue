<script>
export default {
    props: ["card"]
}
</script>

<template>
    <div class="card">
        <p>{{ card.name }} by {{ card.creator }}</p>
        <img v-bind:src="`http://127.0.0.1:5000${card.image_path}`" />
        <p>
            Riddle: {{ card.riddle }}
            <br />
            Solution: {{ card.solution }}
        </p>
    </div>
</template>

<style>
.test {
    width: 50%
}
</style>