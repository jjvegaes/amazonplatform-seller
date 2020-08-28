from advertising_api import AdvertisingApi



if __name__ == "__main__":
    client_id = "amzn1.application-oa2-client.a8fd6816f08d46569dfd2362198fc4d1"
    client_secret = "a743f8e758089168f35bfbc5bc3399567ae8e8e95dbeddc5fc17ecf7de2532de"
    region = 'eu'
    refresh_token = "Atzr|IwEBIEYT9CTs1wjqY_2BmAtJ4Qe48rXZedBiMXLA9CbPiQp18-oyNQlLMEyYxSEUXuwbqwQuGL6X-8B9Ed2QufqJydIxkVsp4eOxA2Fu2fNJkp6T8ksjkqUiM-8k4JxgX1ETahTDlq21dHuDRK4G8LhtlYe8D9aMDViJdHcGcb3ctyli8_xKX1xLjKg8YQRloB01OZLfjrhp1a-0n76K1gUhmPuU4zIhm8Ap8bgMBjwtUR-xSEo50nKUAmq9BCyDHM6AfYWTSBwXUrJmdMBOWDfT6E6Qd7r0nuT3n4Flhgs2mSNjznNYUk6sOOgPjaif0lK8sd5tr2b2cvoJ3nQsupiPBvqOhZvIn_NYMLIBF4iI4oYDpc9fTlFG8ZVT-JDFJyFvzCIZhePHvt1elcaomZvRp_f1Z-EXxCPenQxKn_cWtMpf90q4m8ULiLQ5eNh09m_Fh3Y"
    adAPI = AdvertisingApi(client_id, client_secret, region, "Atza|IwEBIHQTWQ2o834DTAzEwvIHyZ7XvhfMmeHwN91WQ0lvlN8R6k5f9ZUOR0I2jUyP4-ld2bxxQWUN99thGwg-3zt3O5szdE97fgRQ6esu6gNK3APQW8UwsYd6NrTFRtONbxiKXHEbj1DtteZAM0JvkV9LuxyCD83lZLjEagRReK0zDdDjcvk_WQa8Ap3rUu0Rxd2acG7nLikegqkx5Er55HSgBzbHgjzXnp1uWsv0f_MxW2mcw0dAQqdTQh5gSt2X0-OzP8sO3CT1gSMSFm-72OFZL0DYmhi6FPhDBspLdfHldkLFCEiKtP5-edB7TXBnypE-QOC168s33Q6wxqNSNbNafJjAyRegK8Hy9mIjMnV79zL39Olmd6MMxDW2bl244Wmyqw1HeO8YD0A3vj0YIkL7dJw1SwKxyRiJvCxjKegc9EzHYg", refresh_token= refresh_token)
    
    adAPI.do_refresh_token()
    print(adAPI.access_token)

    print(adAPI.list_campaigns())