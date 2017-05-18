'''
    The idea of this code is to make requests to the MusicBrainz api,
    in order to obtain the mbids of all string quartets (and each movement)
    from Mozart, Beethoven and Haydn, and organize that information in a
    python dictionary, for future uses.

    Common definitions about the string quartets

    Nestor Napoles, December 2016
    nestor.napoles@upf.edu
'''

# MusicBrainz ID of Joseph Haydn
haydn_mbid = 'c130b0fb-5dce-449d-9f40-1437f889f7fe'
# MusicBrainz ID of Amadeus Mozart
mozart_mbid = 'b972f589-fb0e-474e-b64a-803b0364fa75'
# MusicBrainz ID of Ludwig van Beethoven
beethoven_mbid = '1f9df192-a621-4f54-8850-2c5373b7eac9'

# Manually-checked quartet lists by Rafael Caro
manual_quartet_lists = {
haydn_mbid: [
'84fd8aea-d8dc-483b-ae3f-6925cce9ab9c',
'7da8947b-d6f9-4d12-9607-f3c13d5b2687',
'6f34b308-54fc-4b8b-8eb4-b2e6e56d4581',
'2a138700-cb76-4d1c-8426-ca5cb3d5c4dd',
'20dd0718-3da2-4dfb-ae0a-04664c57dbe5',
'12ee33f5-8216-403d-b0f5-324971dd422b'
],
beethoven_mbid: [
'd1f556cb-d8a0-4b84-800f-e28ec489c7cc',
'fc9651a1-ca09-4e74-aaeb-fbbf01ae8181',
'0c2937a5-73e7-4a90-856b-878df5879a79',
'3758f33c-1d85-4c1c-bd57-1f70fd4e9ad1',
'1d891907-08cf-4528-9061-73786e3f6975',
'76de79fa-71f2-4178-9e01-9a0015826031',
'9833ed4b-e167-40c5-8ef4-6775bed7444e',
'aa6befc6-32ba-4692-87d8-15bd67ae7290',
'297b54c8-03f8-49ea-8288-a5421e059e20',
'fdb3af54-4c10-4c8d-9147-0e7c3400f7cc',
'8883f4bf-8760-4f48-a158-e0a2b72c6657',
'6472a326-4143-46f3-b302-829553e97d7b',
'56fc7235-9483-4f8e-beda-e11197e507e1',
'7ce0f214-f37a-407e-907d-2a4ab7a80757',
'2638304f-0c71-40e6-9572-375c85e1cdf4',
#'cc6eba78-85ef-3834-a400-a34e0d8856d9',  Grosse Fugue
'4d973e8d-37c0-4709-ad45-1fff7a014f65'
],
mozart_mbid: [
'88e47097-5b7d-4c5f-8e1e-f5a7b69183f9',
'066b9d77-7484-48a9-9910-983badd4a24a',
'1567f292-abe5-44a7-b2ac-1f7ee38d37e6',
'1ae6b6c7-d93f-4263-bcad-07a0d0b6377e',
'b259ae64-77b9-413b-8eeb-84b61bd73fb9',
'a2a0f4c9-91d2-46fd-8246-003d659b985f',
'70c4dbc5-4a09-4195-9739-459315855476',
'32a8c980-3b89-4cd8-94b7-f4cee7d1eb30',
'bc779420-dd7a-4b2d-8d37-fefd27f36674',
'80b390e6-7e28-4166-aa41-3296eec31139',
'1adc928e-f218-4734-81c8-104e7262b0a5',
'5f75254b-d066-4316-bb01-2e9afb91de6f',
'd764368c-06d9-4bf9-b19d-7f6d54cc3e65',
'd7646788-846b-46ae-926c-2e3de4653544',
'060cf3e7-50d8-4259-9254-6456a2bc713f',
'6b5ae252-71d8-438c-a30b-56901efa191a',
'e69f07fe-fb06-3ef5-9739-8197ac7bd33e',
'8a265531-1344-4a46-b4d5-bcfa64fba2a4',
'4d9a78f9-ac5d-4ef5-9650-cb3418c93da9',
'669a936a-48c4-48fc-a02f-d61971f416d3',
'bc1999aa-3826-438e-8e8e-5c42dffa519e',
'6a1b83fb-76e3-44dd-8fb1-fe16831f85d6',
'2652f219-4aa6-4721-b8da-c02d3d095a6c'
]
}
