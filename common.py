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
'c0201a3a-c643-48dc-ae62-6edc1ced17b4',
'4901c365-83a8-42f1-949c-21ca6cc2beeb',
'7030ad31-a81e-4390-b24c-a7b42019a176',
'74129350-e7da-46e2-840e-0a4bb919bb07',
'3df69c62-1244-40e3-82ae-43e29a52d663',
'd685aebf-4d2d-4f6d-9544-288b80873bc5',
'e3126e71-88ac-4d74-87c1-8e0fbeb67043',
'35b0ea87-07c5-48b5-abfc-e6a3cb0110c4',
'36d3201e-efc1-4d75-bf3f-f397629d0cc8',
'9ecd4cbf-59a0-4f06-b9e9-5c39f824c8c8',
'78140e8d-eace-4ca3-9246-d50595ca8edf',
'2f518606-6d69-48ec-8922-e76591346e91',
'b4865541-eab5-450e-9dfa-e7fd97ecdfe3',
'ec11c1d7-5142-4f59-bfb9-1eb9b6711ce9',
'6f2f42fe-80b4-4654-8e31-2eb3fea98264',
'47262003-162b-4e83-8784-0fdd0300fe2a',
'e71e5bef-640f-42f7-8a18-cfa9d48bd7f3',
'725918d3-b26f-420f-bab0-29eb6332a8fa',
'20bc8ed4-6062-4815-9287-fcfd2ddb42dc',
'a0345283-7de8-48d5-b249-f3832fd88024',
'bb9f23e0-f6f2-4948-ba93-32b63c4febd4',
'bfb3941f-2f1b-4d38-a35b-59db30df407d',
'84fd8aea-d8dc-483b-ae3f-6925cce9ab9c',
'7da8947b-d6f9-4d12-9607-f3c13d5b2687',
'6f34b308-54fc-4b8b-8eb4-b2e6e56d4581',
'2a138700-cb76-4d1c-8426-ca5cb3d5c4dd',
'20dd0718-3da2-4dfb-ae0a-04664c57dbe5',
'12ee33f5-8216-403d-b0f5-324971dd422b',
'fa0369fe-e1df-4766-b763-11e784d8a395',
'3856c58a-4b21-4633-ac58-80dd6d312c9a',
'b20de149-d11a-471e-825e-dd0957a29656',
'22fd1ef9-4f44-45c5-8cfb-c6f7c7ef0ca4',
'e5c02749-9950-4bac-8e84-07162d5fb35e',
'a80cd213-8f07-4065-b303-43e290f7f86f',
'30dc2817-c536-43ff-8600-8ac168d55ea4',
'c2ca24b5-610d-496d-b174-fbc5108b9fa3',
'3a0d32b7-027c-4d53-a96f-867c9fe4add9',
'8a9ca66a-c2d1-4568-bce7-314253848b4f',
'8bd67b40-adfb-4949-8c0d-7de981c7cfcb',
'4965e4db-4daf-4837-ae79-cacaaef3811a',
'9aa980c2-6c16-4dc4-99aa-b3e8e21a643d',
'248ebb3a-d700-4b24-ac4e-ac14be01d0ff',
'6b3ced65-acee-4c01-a4b0-634b7825fe13',
'5039fdf2-0550-424b-93a7-badd5a566cc6',
'dfafbc4d-f874-4f68-afd2-13fa7292a7dd',
'cb3fb6fa-6866-43b3-8f51-88cff89d31e6',
'fda7b6b5-e548-4927-9b52-67f011cd5ec7',
'8d0ff591-0463-45ed-961a-176c035b2c26',
'f405e509-35a9-49ea-9889-e668a15d3e58',
'85940de4-8435-4aae-8676-73a6361f1e8f',
'5f39987a-c0ee-4909-b9f2-d29f9570ef43',
'da4c8176-af9f-4f2f-bc90-ff7231b9d466',
'fbe1fabd-8d31-427f-b770-f64b4445cd80',
'70c26698-a740-492f-8468-f07c1adc7107',
'49ed06b2-e6ee-4fc6-843b-9a498e27dcc6',
'a49a6274-ac9c-415b-bd72-ead36e2f5f80',
'0f199584-4e0f-4352-9228-f852b8ab2ffd',
'109a2deb-30e1-43a5-a173-d658f9ebce97',
'68750762-33f8-4813-ae09-8788ddbc0773',
'924aa7f5-3e70-44b9-900b-b5ca88aba342',
'bcecb3f4-07fb-4af0-982d-78ea66748d2f',
'efe6cde8-613c-4a7c-8079-18223093be83',
'a723b328-ae25-4f0e-ad92-d6423f31b4ab',
'e6abe975-8385-4254-b0db-ffa990c47a21',
'ab5c4a3b-53be-41ad-9a9e-406081bce450',
'a0e158de-be05-43c3-b06f-9398b6265f35',
'f80062d0-0a43-416d-9791-d6127cc084f7',
'09431718-8819-4d1c-95cf-9a53a2a4de48'
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
