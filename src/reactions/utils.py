async def get_all_reactions(post_reactions):
    reactions = []

    if len(post_reactions) != 0:
        for reaction in post_reactions:
            reactions.append(reaction[0])

    return reactions
