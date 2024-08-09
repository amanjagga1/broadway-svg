import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon
import numpy as np
from scipy.spatial import Delaunay
from shapely.geometry import Polygon, MultiPolygon, LineString
from shapely.ops import cascaded_union, polygonize

points = [
      {
        "seat": {
          "cx": "257",
          "cy": "268",
          "r": "6",
          "class": "seat-orchestra-k-101"
        },
        "cx": 257.0,
        "cy": 268.0
      },
      {
        "seat": {
          "cx": "270",
          "cy": "274",
          "r": "6",
          "class": "seat-orchestra-k-102"
        },
        "cx": 270.0,
        "cy": 274.0
      },
      {
        "seat": {
          "cx": "283",
          "cy": "280",
          "r": "6",
          "class": "seat-orchestra-k-103"
        },
        "cx": 283.0,
        "cy": 280.0
      },
      {
        "seat": {
          "cx": "296",
          "cy": "285",
          "r": "6",
          "class": "seat-orchestra-k-104"
        },
        "cx": 296.0,
        "cy": 285.0
      },
      {
        "seat": {
          "cx": "309",
          "cy": "289",
          "r": "6",
          "class": "seat-orchestra-k-105"
        },
        "cx": 309.0,
        "cy": 289.0
      },
      {
        "seat": {
          "cx": "322",
          "cy": "293",
          "r": "6",
          "class": "seat-orchestra-k-106"
        },
        "cx": 322.0,
        "cy": 293.0
      },
      {
        "seat": {
          "cx": "335",
          "cy": "296",
          "r": "6",
          "class": "seat-orchestra-k-107"
        },
        "cx": 335.0,
        "cy": 296.0
      },
      {
        "seat": {
          "cx": "348",
          "cy": "299",
          "r": "6",
          "class": "seat-orchestra-k-108"
        },
        "cx": 348.0,
        "cy": 299.0
      },
      {
        "seat": {
          "cx": "361",
          "cy": "301",
          "r": "6",
          "class": "seat-orchestra-k-109"
        },
        "cx": 361.0,
        "cy": 301.0
      },
      {
        "seat": {
          "cx": "263",
          "cy": "254",
          "r": "6",
          "class": "seat-orchestra-j-101"
        },
        "cx": 263.0,
        "cy": 254.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "260",
          "r": "6",
          "class": "seat-orchestra-j-102"
        },
        "cx": 276.0,
        "cy": 260.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "265",
          "r": "6",
          "class": "seat-orchestra-j-103"
        },
        "cx": 289.0,
        "cy": 265.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "270",
          "r": "6",
          "class": "seat-orchestra-j-104"
        },
        "cx": 302.0,
        "cy": 270.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "274",
          "r": "6",
          "class": "seat-orchestra-j-105"
        },
        "cx": 315.0,
        "cy": 274.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "278",
          "r": "6",
          "class": "seat-orchestra-j-106"
        },
        "cx": 328.0,
        "cy": 278.0
      },
      {
        "seat": {
          "cx": "341",
          "cy": "281",
          "r": "6",
          "class": "seat-orchestra-j-107"
        },
        "cx": 341.0,
        "cy": 281.0
      },
      {
        "seat": {
          "cx": "354",
          "cy": "283",
          "r": "6",
          "class": "seat-orchestra-j-108"
        },
        "cx": 354.0,
        "cy": 283.0
      },
      {
        "seat": {
          "cx": "269",
          "cy": "240",
          "r": "6",
          "class": "seat-orchestra-h-101"
        },
        "cx": 269.0,
        "cy": 240.0
      },
      {
        "seat": {
          "cx": "282",
          "cy": "246",
          "r": "6",
          "class": "seat-orchestra-h-102"
        },
        "cx": 282.0,
        "cy": 246.0
      },
      {
        "seat": {
          "cx": "295",
          "cy": "251",
          "r": "6",
          "class": "seat-orchestra-h-103"
        },
        "cx": 295.0,
        "cy": 251.0
      },
      {
        "seat": {
          "cx": "308",
          "cy": "255",
          "r": "6",
          "class": "seat-orchestra-h-104"
        },
        "cx": 308.0,
        "cy": 255.0
      },
      {
        "seat": {
          "cx": "321",
          "cy": "259",
          "r": "6",
          "class": "seat-orchestra-h-105"
        },
        "cx": 321.0,
        "cy": 259.0
      },
      {
        "seat": {
          "cx": "334",
          "cy": "262",
          "r": "6",
          "class": "seat-orchestra-h-106"
        },
        "cx": 334.0,
        "cy": 262.0
      },
      {
        "seat": {
          "cx": "347",
          "cy": "265",
          "r": "6",
          "class": "seat-orchestra-h-107"
        },
        "cx": 347.0,
        "cy": 265.0
      },
      {
        "seat": {
          "cx": "360",
          "cy": "267",
          "r": "6",
          "class": "seat-orchestra-h-108"
        },
        "cx": 360.0,
        "cy": 267.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "227",
          "r": "6",
          "class": "seat-orchestra-g-101"
        },
        "cx": 276.0,
        "cy": 227.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "232",
          "r": "6",
          "class": "seat-orchestra-g-102"
        },
        "cx": 289.0,
        "cy": 232.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "237",
          "r": "6",
          "class": "seat-orchestra-g-103"
        },
        "cx": 302.0,
        "cy": 237.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "241",
          "r": "6",
          "class": "seat-orchestra-g-104"
        },
        "cx": 315.0,
        "cy": 241.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "244",
          "r": "6",
          "class": "seat-orchestra-g-105"
        },
        "cx": 328.0,
        "cy": 244.0
      },
      {
        "seat": {
          "cx": "341",
          "cy": "247",
          "r": "6",
          "class": "seat-orchestra-g-106"
        },
        "cx": 341.0,
        "cy": 247.0
      },
      {
        "seat": {
          "cx": "354",
          "cy": "250",
          "r": "6",
          "class": "seat-orchestra-g-107"
        },
        "cx": 354.0,
        "cy": 250.0
      },
      {
        "seat": {
          "cx": "367",
          "cy": "252",
          "r": "6",
          "class": "seat-orchestra-g-108"
        },
        "cx": 367.0,
        "cy": 252.0
      },
      {
        "seat": {
          "cx": "282",
          "cy": "213",
          "r": "6",
          "class": "seat-orchestra-f-101"
        },
        "cx": 282.0,
        "cy": 213.0
      },
      {
        "seat": {
          "cx": "295",
          "cy": "218",
          "r": "6",
          "class": "seat-orchestra-f-102"
        },
        "cx": 295.0,
        "cy": 218.0
      },
      {
        "seat": {
          "cx": "308",
          "cy": "222",
          "r": "6",
          "class": "seat-orchestra-f-103"
        },
        "cx": 308.0,
        "cy": 222.0
      },
      {
        "seat": {
          "cx": "321",
          "cy": "226",
          "r": "6",
          "class": "seat-orchestra-f-104"
        },
        "cx": 321.0,
        "cy": 226.0
      },
      {
        "seat": {
          "cx": "334",
          "cy": "229",
          "r": "6",
          "class": "seat-orchestra-f-105"
        },
        "cx": 334.0,
        "cy": 229.0
      },
      {
        "seat": {
          "cx": "347",
          "cy": "232",
          "r": "6",
          "class": "seat-orchestra-f-106"
        },
        "cx": 347.0,
        "cy": 232.0
      },
      {
        "seat": {
          "cx": "360",
          "cy": "234",
          "r": "6",
          "class": "seat-orchestra-f-107"
        },
        "cx": 360.0,
        "cy": 234.0
      },
      {
        "seat": {
          "cx": "295",
          "cy": "201",
          "r": "6",
          "class": "seat-orchestra-e-101"
        },
        "cx": 295.0,
        "cy": 201.0
      },
      {
        "seat": {
          "cx": "308",
          "cy": "205",
          "r": "6",
          "class": "seat-orchestra-e-102"
        },
        "cx": 308.0,
        "cy": 205.0
      },
      {
        "seat": {
          "cx": "321",
          "cy": "208",
          "r": "6",
          "class": "seat-orchestra-e-103"
        },
        "cx": 321.0,
        "cy": 208.0
      },
      {
        "seat": {
          "cx": "334",
          "cy": "212",
          "r": "6",
          "class": "seat-orchestra-e-104"
        },
        "cx": 334.0,
        "cy": 212.0
      },
      {
        "seat": {
          "cx": "347",
          "cy": "215",
          "r": "6",
          "class": "seat-orchestra-e-105"
        },
        "cx": 347.0,
        "cy": 215.0
      },
      {
        "seat": {
          "cx": "360",
          "cy": "217",
          "r": "6",
          "class": "seat-orchestra-e-106"
        },
        "cx": 360.0,
        "cy": 217.0
      },
      {
        "seat": {
          "cx": "373",
          "cy": "219",
          "r": "6",
          "class": "seat-orchestra-e-107"
        },
        "cx": 373.0,
        "cy": 219.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "187",
          "r": "6",
          "class": "seat-orchestra-d-101"
        },
        "cx": 302.0,
        "cy": 187.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "191",
          "r": "6",
          "class": "seat-orchestra-d-102"
        },
        "cx": 315.0,
        "cy": 191.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "194",
          "r": "6",
          "class": "seat-orchestra-d-103"
        },
        "cx": 328.0,
        "cy": 194.0
      },
      {
        "seat": {
          "cx": "341",
          "cy": "197",
          "r": "6",
          "class": "seat-orchestra-d-104"
        },
        "cx": 341.0,
        "cy": 197.0
      },
      {
        "seat": {
          "cx": "354",
          "cy": "200",
          "r": "6",
          "class": "seat-orchestra-d-105"
        },
        "cx": 354.0,
        "cy": 200.0
      },
      {
        "seat": {
          "cx": "367",
          "cy": "202",
          "r": "6",
          "class": "seat-orchestra-d-106"
        },
        "cx": 367.0,
        "cy": 202.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "174",
          "r": "6",
          "class": "seat-orchestra-c-101"
        },
        "cx": 315.0,
        "cy": 174.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "177",
          "r": "6",
          "class": "seat-orchestra-c-102"
        },
        "cx": 328.0,
        "cy": 177.0
      },
      {
        "seat": {
          "cx": "341",
          "cy": "181",
          "r": "6",
          "class": "seat-orchestra-c-103"
        },
        "cx": 341.0,
        "cy": 181.0
      },
      {
        "seat": {
          "cx": "354",
          "cy": "183",
          "r": "6",
          "class": "seat-orchestra-c-104"
        },
        "cx": 354.0,
        "cy": 183.0
      },
      {
        "seat": {
          "cx": "367",
          "cy": "185",
          "r": "6",
          "class": "seat-orchestra-c-105"
        },
        "cx": 367.0,
        "cy": 185.0
      },
      {
        "seat": {
          "cx": "380",
          "cy": "187",
          "r": "6",
          "class": "seat-orchestra-c-106"
        },
        "cx": 380.0,
        "cy": 187.0
      },
      {
        "seat": {
          "cx": "321",
          "cy": "159",
          "r": "6",
          "class": "seat-orchestra-b-101"
        },
        "cx": 321.0,
        "cy": 159.0
      },
      {
        "seat": {
          "cx": "334",
          "cy": "162",
          "r": "6",
          "class": "seat-orchestra-b-102"
        },
        "cx": 334.0,
        "cy": 162.0
      },
      {
        "seat": {
          "cx": "347",
          "cy": "165",
          "r": "6",
          "class": "seat-orchestra-b-103"
        },
        "cx": 347.0,
        "cy": 165.0
      },
      {
        "seat": {
          "cx": "360",
          "cy": "167",
          "r": "6",
          "class": "seat-orchestra-b-104"
        },
        "cx": 360.0,
        "cy": 167.0
      },
      {
        "seat": {
          "cx": "373",
          "cy": "169",
          "r": "6",
          "class": "seat-orchestra-b-105"
        },
        "cx": 373.0,
        "cy": 169.0
      },
      {
        "seat": {
          "cx": "334",
          "cy": "146",
          "r": "6",
          "class": "seat-orchestra-a-101"
        },
        "cx": 334.0,
        "cy": 146.0
      },
      {
        "seat": {
          "cx": "347",
          "cy": "149",
          "r": "6",
          "class": "seat-orchestra-a-102"
        },
        "cx": 347.0,
        "cy": 149.0
      },
      {
        "seat": {
          "cx": "360",
          "cy": "151",
          "r": "6",
          "class": "seat-orchestra-a-103"
        },
        "cx": 360.0,
        "cy": 151.0
      },
      {
        "seat": {
          "cx": "373",
          "cy": "153",
          "r": "6",
          "class": "seat-orchestra-a-104"
        },
        "cx": 373.0,
        "cy": 153.0
      },
      {
        "seat": {
          "cx": "386",
          "cy": "155",
          "r": "6",
          "class": "seat-orchestra-a-105"
        },
        "cx": 386.0,
        "cy": 155.0
      },
      {
        "seat": {
          "cx": "237",
          "cy": "412",
          "r": "6",
          "class": "seat-orchestra-t-101"
        },
        "cx": 237.0,
        "cy": 412.0
      },
      {
        "seat": {
          "cx": "250",
          "cy": "420",
          "r": "6",
          "class": "seat-orchestra-t-102"
        },
        "cx": 250.0,
        "cy": 420.0
      },
      {
        "seat": {
          "cx": "263",
          "cy": "426",
          "r": "6",
          "class": "seat-orchestra-t-103"
        },
        "cx": 263.0,
        "cy": 426.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "432",
          "r": "6",
          "class": "seat-orchestra-t-104"
        },
        "cx": 276.0,
        "cy": 432.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "437",
          "r": "6",
          "class": "seat-orchestra-t-105"
        },
        "cx": 289.0,
        "cy": 437.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "442",
          "r": "6",
          "class": "seat-orchestra-t-106"
        },
        "cx": 302.0,
        "cy": 442.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "446",
          "r": "6",
          "class": "seat-orchestra-t-107"
        },
        "cx": 315.0,
        "cy": 446.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "450",
          "r": "6",
          "class": "seat-orchestra-t-108"
        },
        "cx": 328.0,
        "cy": 450.0
      },
      {
        "seat": {
          "cx": "341",
          "cy": "453",
          "r": "6",
          "class": "seat-orchestra-t-109"
        },
        "cx": 341.0,
        "cy": 453.0
      },
      {
        "seat": {
          "cx": "354",
          "cy": "455",
          "r": "6",
          "class": "seat-orchestra-t-110"
        },
        "cx": 354.0,
        "cy": 455.0
      },
      {
        "seat": {
          "cx": "237",
          "cy": "395",
          "r": "6",
          "class": "seat-orchestra-s-101"
        },
        "cx": 237.0,
        "cy": 395.0
      },
      {
        "seat": {
          "cx": "250",
          "cy": "403",
          "r": "6",
          "class": "seat-orchestra-s-102"
        },
        "cx": 250.0,
        "cy": 403.0
      },
      {
        "seat": {
          "cx": "263",
          "cy": "409",
          "r": "6",
          "class": "seat-orchestra-s-103"
        },
        "cx": 263.0,
        "cy": 409.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "415",
          "r": "6",
          "class": "seat-orchestra-s-104"
        },
        "cx": 276.0,
        "cy": 415.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "420",
          "r": "6",
          "class": "seat-orchestra-s-105"
        },
        "cx": 289.0,
        "cy": 420.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "425",
          "r": "6",
          "class": "seat-orchestra-s-106"
        },
        "cx": 302.0,
        "cy": 425.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "429",
          "r": "6",
          "class": "seat-orchestra-s-107"
        },
        "cx": 315.0,
        "cy": 429.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "433",
          "r": "6",
          "class": "seat-orchestra-s-108"
        },
        "cx": 328.0,
        "cy": 433.0
      },
      {
        "seat": {
          "cx": "341",
          "cy": "436",
          "r": "6",
          "class": "seat-orchestra-s-109"
        },
        "cx": 341.0,
        "cy": 436.0
      },
      {
        "seat": {
          "cx": "354",
          "cy": "438",
          "r": "6",
          "class": "seat-orchestra-s-110"
        },
        "cx": 354.0,
        "cy": 438.0
      },
      {
        "seat": {
          "cx": "237",
          "cy": "378",
          "r": "6",
          "class": "seat-orchestra-r-101"
        },
        "cx": 237.0,
        "cy": 378.0
      },
      {
        "seat": {
          "cx": "250",
          "cy": "386",
          "r": "6",
          "class": "seat-orchestra-r-102"
        },
        "cx": 250.0,
        "cy": 386.0
      },
      {
        "seat": {
          "cx": "263",
          "cy": "392",
          "r": "6",
          "class": "seat-orchestra-r-103"
        },
        "cx": 263.0,
        "cy": 392.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "398",
          "r": "6",
          "class": "seat-orchestra-r-104"
        },
        "cx": 276.0,
        "cy": 398.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "403",
          "r": "6",
          "class": "seat-orchestra-r-105"
        },
        "cx": 289.0,
        "cy": 403.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "408",
          "r": "6",
          "class": "seat-orchestra-r-106"
        },
        "cx": 302.0,
        "cy": 408.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "412",
          "r": "6",
          "class": "seat-orchestra-r-107"
        },
        "cx": 315.0,
        "cy": 412.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "416",
          "r": "6",
          "class": "seat-orchestra-r-108"
        },
        "cx": 328.0,
        "cy": 416.0
      },
      {
        "seat": {
          "cx": "341",
          "cy": "419",
          "r": "6",
          "class": "seat-orchestra-r-109"
        },
        "cx": 341.0,
        "cy": 419.0
      },
      {
        "seat": {
          "cx": "354",
          "cy": "421",
          "r": "6",
          "class": "seat-orchestra-r-110"
        },
        "cx": 354.0,
        "cy": 421.0
      },
      {
        "seat": {
          "cx": "237",
          "cy": "361",
          "r": "6",
          "class": "seat-orchestra-q-101"
        },
        "cx": 237.0,
        "cy": 361.0
      },
      {
        "seat": {
          "cx": "250",
          "cy": "369",
          "r": "6",
          "class": "seat-orchestra-q-102"
        },
        "cx": 250.0,
        "cy": 369.0
      },
      {
        "seat": {
          "cx": "263",
          "cy": "375",
          "r": "6",
          "class": "seat-orchestra-q-103"
        },
        "cx": 263.0,
        "cy": 375.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "381",
          "r": "6",
          "class": "seat-orchestra-q-104"
        },
        "cx": 276.0,
        "cy": 381.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "386",
          "r": "6",
          "class": "seat-orchestra-q-105"
        },
        "cx": 289.0,
        "cy": 386.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "391",
          "r": "6",
          "class": "seat-orchestra-q-106"
        },
        "cx": 302.0,
        "cy": 391.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "395",
          "r": "6",
          "class": "seat-orchestra-q-107"
        },
        "cx": 315.0,
        "cy": 395.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "399",
          "r": "6",
          "class": "seat-orchestra-q-108"
        },
        "cx": 328.0,
        "cy": 399.0
      },
      {
        "seat": {
          "cx": "341",
          "cy": "402",
          "r": "6",
          "class": "seat-orchestra-q-109"
        },
        "cx": 341.0,
        "cy": 402.0
      },
      {
        "seat": {
          "cx": "354",
          "cy": "404",
          "r": "6",
          "class": "seat-orchestra-q-110"
        },
        "cx": 354.0,
        "cy": 404.0
      },
      {
        "seat": {
          "cx": "237",
          "cy": "344",
          "r": "6",
          "class": "seat-orchestra-p-101"
        },
        "cx": 237.0,
        "cy": 344.0
      },
      {
        "seat": {
          "cx": "250",
          "cy": "352",
          "r": "6",
          "class": "seat-orchestra-p-102"
        },
        "cx": 250.0,
        "cy": 352.0
      },
      {
        "seat": {
          "cx": "263",
          "cy": "358",
          "r": "6",
          "class": "seat-orchestra-p-103"
        },
        "cx": 263.0,
        "cy": 358.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "364",
          "r": "6",
          "class": "seat-orchestra-p-104"
        },
        "cx": 276.0,
        "cy": 364.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "369",
          "r": "6",
          "class": "seat-orchestra-p-105"
        },
        "cx": 289.0,
        "cy": 369.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "374",
          "r": "6",
          "class": "seat-orchestra-p-106"
        },
        "cx": 302.0,
        "cy": 374.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "378",
          "r": "6",
          "class": "seat-orchestra-p-107"
        },
        "cx": 315.0,
        "cy": 378.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "382",
          "r": "6",
          "class": "seat-orchestra-p-108"
        },
        "cx": 328.0,
        "cy": 382.0
      },
      {
        "seat": {
          "cx": "341",
          "cy": "385",
          "r": "6",
          "class": "seat-orchestra-p-109"
        },
        "cx": 341.0,
        "cy": 385.0
      },
      {
        "seat": {
          "cx": "354",
          "cy": "387",
          "r": "6",
          "class": "seat-orchestra-p-110"
        },
        "cx": 354.0,
        "cy": 387.0
      },
      {
        "seat": {
          "cx": "237",
          "cy": "327",
          "r": "6",
          "class": "seat-orchestra-o-101"
        },
        "cx": 237.0,
        "cy": 327.0
      },
      {
        "seat": {
          "cx": "250",
          "cy": "335",
          "r": "6",
          "class": "seat-orchestra-o-102"
        },
        "cx": 250.0,
        "cy": 335.0
      },
      {
        "seat": {
          "cx": "263",
          "cy": "341",
          "r": "6",
          "class": "seat-orchestra-o-103"
        },
        "cx": 263.0,
        "cy": 341.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "347",
          "r": "6",
          "class": "seat-orchestra-o-104"
        },
        "cx": 276.0,
        "cy": 347.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "352",
          "r": "6",
          "class": "seat-orchestra-o-105"
        },
        "cx": 289.0,
        "cy": 352.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "357",
          "r": "6",
          "class": "seat-orchestra-o-106"
        },
        "cx": 302.0,
        "cy": 357.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "361",
          "r": "6",
          "class": "seat-orchestra-o-107"
        },
        "cx": 315.0,
        "cy": 361.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "365",
          "r": "6",
          "class": "seat-orchestra-o-108"
        },
        "cx": 328.0,
        "cy": 365.0
      },
      {
        "seat": {
          "cx": "341",
          "cy": "368",
          "r": "6",
          "class": "seat-orchestra-o-109"
        },
        "cx": 341.0,
        "cy": 368.0
      },
      {
        "seat": {
          "cx": "354",
          "cy": "370",
          "r": "6",
          "class": "seat-orchestra-o-110"
        },
        "cx": 354.0,
        "cy": 370.0
      },
      {
        "seat": {
          "cx": "237",
          "cy": "310",
          "r": "6",
          "class": "seat-orchestra-n-101"
        },
        "cx": 237.0,
        "cy": 310.0
      },
      {
        "seat": {
          "cx": "250",
          "cy": "318",
          "r": "6",
          "class": "seat-orchestra-n-102"
        },
        "cx": 250.0,
        "cy": 318.0
      },
      {
        "seat": {
          "cx": "263",
          "cy": "324",
          "r": "6",
          "class": "seat-orchestra-n-103"
        },
        "cx": 263.0,
        "cy": 324.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "330",
          "r": "6",
          "class": "seat-orchestra-n-104"
        },
        "cx": 276.0,
        "cy": 330.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "335",
          "r": "6",
          "class": "seat-orchestra-n-105"
        },
        "cx": 289.0,
        "cy": 335.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "340",
          "r": "6",
          "class": "seat-orchestra-n-106"
        },
        "cx": 302.0,
        "cy": 340.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "344",
          "r": "6",
          "class": "seat-orchestra-n-107"
        },
        "cx": 315.0,
        "cy": 344.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "348",
          "r": "6",
          "class": "seat-orchestra-n-108"
        },
        "cx": 328.0,
        "cy": 348.0
      },
      {
        "seat": {
          "cx": "341",
          "cy": "351",
          "r": "6",
          "class": "seat-orchestra-n-109"
        },
        "cx": 341.0,
        "cy": 351.0
      },
      {
        "seat": {
          "cx": "354",
          "cy": "353",
          "r": "6",
          "class": "seat-orchestra-n-110"
        },
        "cx": 354.0,
        "cy": 353.0
      },
      {
        "seat": {
          "cx": "243",
          "cy": "296",
          "r": "6",
          "class": "seat-orchestra-m-101"
        },
        "cx": 243.0,
        "cy": 296.0
      },
      {
        "seat": {
          "cx": "256",
          "cy": "303",
          "r": "6",
          "class": "seat-orchestra-m-102"
        },
        "cx": 256.0,
        "cy": 303.0
      },
      {
        "seat": {
          "cx": "269",
          "cy": "309",
          "r": "6",
          "class": "seat-orchestra-m-103"
        },
        "cx": 269.0,
        "cy": 309.0
      },
      {
        "seat": {
          "cx": "282",
          "cy": "315",
          "r": "6",
          "class": "seat-orchestra-m-104"
        },
        "cx": 282.0,
        "cy": 315.0
      },
      {
        "seat": {
          "cx": "295",
          "cy": "320",
          "r": "6",
          "class": "seat-orchestra-m-105"
        },
        "cx": 295.0,
        "cy": 320.0
      },
      {
        "seat": {
          "cx": "308",
          "cy": "324",
          "r": "6",
          "class": "seat-orchestra-m-106"
        },
        "cx": 308.0,
        "cy": 324.0
      },
      {
        "seat": {
          "cx": "321",
          "cy": "328",
          "r": "6",
          "class": "seat-orchestra-m-107"
        },
        "cx": 321.0,
        "cy": 328.0
      },
      {
        "seat": {
          "cx": "334",
          "cy": "331",
          "r": "6",
          "class": "seat-orchestra-m-108"
        },
        "cx": 334.0,
        "cy": 331.0
      },
      {
        "seat": {
          "cx": "347",
          "cy": "334",
          "r": "6",
          "class": "seat-orchestra-m-109"
        },
        "cx": 347.0,
        "cy": 334.0
      },
      {
        "seat": {
          "cx": "250",
          "cy": "283",
          "r": "6",
          "class": "seat-orchestra-l-101"
        },
        "cx": 250.0,
        "cy": 283.0
      },
      {
        "seat": {
          "cx": "263",
          "cy": "289",
          "r": "6",
          "class": "seat-orchestra-l-102"
        },
        "cx": 263.0,
        "cy": 289.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "295",
          "r": "6",
          "class": "seat-orchestra-l-103"
        },
        "cx": 276.0,
        "cy": 295.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "300",
          "r": "6",
          "class": "seat-orchestra-l-104"
        },
        "cx": 289.0,
        "cy": 300.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "305",
          "r": "6",
          "class": "seat-orchestra-l-105"
        },
        "cx": 302.0,
        "cy": 305.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "309",
          "r": "6",
          "class": "seat-orchestra-l-106"
        },
        "cx": 315.0,
        "cy": 309.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "313",
          "r": "6",
          "class": "seat-orchestra-l-107"
        },
        "cx": 328.0,
        "cy": 313.0
      },
      {
        "seat": {
          "cx": "341",
          "cy": "316",
          "r": "6",
          "class": "seat-orchestra-l-108"
        },
        "cx": 341.0,
        "cy": 316.0
      },
      {
        "seat": {
          "cx": "354",
          "cy": "318",
          "r": "6",
          "class": "seat-orchestra-l-109"
        },
        "cx": 354.0,
        "cy": 318.0
      },
      {
        "seat": {
          "cx": "237",
          "cy": "565",
          "r": "6",
          "class": "seat-orchestra-zzz-101"
        },
        "cx": 237.0,
        "cy": 565.0
      },
      {
        "seat": {
          "cx": "250",
          "cy": "573",
          "r": "6",
          "class": "seat-orchestra-zzz-102"
        },
        "cx": 250.0,
        "cy": 573.0
      },
      {
        "seat": {
          "cx": "263",
          "cy": "579",
          "r": "6",
          "class": "seat-orchestra-zzz-103"
        },
        "cx": 263.0,
        "cy": 579.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "585",
          "r": "6",
          "class": "seat-orchestra-zzz-104"
        },
        "cx": 276.0,
        "cy": 585.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "590",
          "r": "6",
          "class": "seat-orchestra-zzz-105"
        },
        "cx": 289.0,
        "cy": 590.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "595",
          "r": "6",
          "class": "seat-orchestra-zzz-106"
        },
        "cx": 302.0,
        "cy": 595.0
      },
      {
        "seat": {
          "cx": "237",
          "cy": "548",
          "r": "6",
          "class": "seat-orchestra-zz-101"
        },
        "cx": 237.0,
        "cy": 548.0
      },
      {
        "seat": {
          "cx": "250",
          "cy": "556",
          "r": "6",
          "class": "seat-orchestra-zz-102"
        },
        "cx": 250.0,
        "cy": 556.0
      },
      {
        "seat": {
          "cx": "263",
          "cy": "562",
          "r": "6",
          "class": "seat-orchestra-zz-103"
        },
        "cx": 263.0,
        "cy": 562.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "568",
          "r": "6",
          "class": "seat-orchestra-zz-104"
        },
        "cx": 276.0,
        "cy": 568.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "573",
          "r": "6",
          "class": "seat-orchestra-zz-105"
        },
        "cx": 289.0,
        "cy": 573.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "578",
          "r": "6",
          "class": "seat-orchestra-zz-106"
        },
        "cx": 302.0,
        "cy": 578.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "582",
          "r": "6",
          "class": "seat-orchestra-zz-107"
        },
        "cx": 315.0,
        "cy": 582.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "586",
          "r": "6",
          "class": "seat-orchestra-zz-108"
        },
        "cx": 328.0,
        "cy": 586.0
      },
      {
        "seat": {
          "cx": "237",
          "cy": "531",
          "r": "6",
          "class": "seat-orchestra-yy-101"
        },
        "cx": 237.0,
        "cy": 531.0
      },
      {
        "seat": {
          "cx": "250",
          "cy": "539",
          "r": "6",
          "class": "seat-orchestra-yy-102"
        },
        "cx": 250.0,
        "cy": 539.0
      },
      {
        "seat": {
          "cx": "263",
          "cy": "545",
          "r": "6",
          "class": "seat-orchestra-yy-103"
        },
        "cx": 263.0,
        "cy": 545.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "551",
          "r": "6",
          "class": "seat-orchestra-yy-104"
        },
        "cx": 276.0,
        "cy": 551.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "556",
          "r": "6",
          "class": "seat-orchestra-yy-105"
        },
        "cx": 289.0,
        "cy": 556.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "561",
          "r": "6",
          "class": "seat-orchestra-yy-106"
        },
        "cx": 302.0,
        "cy": 561.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "565",
          "r": "6",
          "class": "seat-orchestra-yy-107"
        },
        "cx": 315.0,
        "cy": 565.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "569",
          "r": "6",
          "class": "seat-orchestra-yy-108"
        },
        "cx": 328.0,
        "cy": 569.0
      },
      {
        "seat": {
          "cx": "237",
          "cy": "514",
          "r": "6",
          "class": "seat-orchestra-z-101"
        },
        "cx": 237.0,
        "cy": 514.0
      },
      {
        "seat": {
          "cx": "250",
          "cy": "522",
          "r": "6",
          "class": "seat-orchestra-z-102"
        },
        "cx": 250.0,
        "cy": 522.0
      },
      {
        "seat": {
          "cx": "263",
          "cy": "528",
          "r": "6",
          "class": "seat-orchestra-z-103"
        },
        "cx": 263.0,
        "cy": 528.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "534",
          "r": "6",
          "class": "seat-orchestra-z-104"
        },
        "cx": 276.0,
        "cy": 534.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "539",
          "r": "6",
          "class": "seat-orchestra-z-105"
        },
        "cx": 289.0,
        "cy": 539.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "544",
          "r": "6",
          "class": "seat-orchestra-z-106"
        },
        "cx": 302.0,
        "cy": 544.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "548",
          "r": "6",
          "class": "seat-orchestra-z-107"
        },
        "cx": 315.0,
        "cy": 548.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "552",
          "r": "6",
          "class": "seat-orchestra-z-108"
        },
        "cx": 328.0,
        "cy": 552.0
      },
      {
        "seat": {
          "cx": "341",
          "cy": "555",
          "r": "6",
          "class": "seat-orchestra-z-109"
        },
        "cx": 341.0,
        "cy": 555.0
      },
      {
        "seat": {
          "cx": "354",
          "cy": "557",
          "r": "6",
          "class": "seat-orchestra-z-110"
        },
        "cx": 354.0,
        "cy": 557.0
      },
      {
        "seat": {
          "cx": "237",
          "cy": "497",
          "r": "6",
          "class": "seat-orchestra-y-101"
        },
        "cx": 237.0,
        "cy": 497.0
      },
      {
        "seat": {
          "cx": "250",
          "cy": "505",
          "r": "6",
          "class": "seat-orchestra-y-102"
        },
        "cx": 250.0,
        "cy": 505.0
      },
      {
        "seat": {
          "cx": "263",
          "cy": "511",
          "r": "6",
          "class": "seat-orchestra-y-103"
        },
        "cx": 263.0,
        "cy": 511.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "517",
          "r": "6",
          "class": "seat-orchestra-y-104"
        },
        "cx": 276.0,
        "cy": 517.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "522",
          "r": "6",
          "class": "seat-orchestra-y-105"
        },
        "cx": 289.0,
        "cy": 522.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "527",
          "r": "6",
          "class": "seat-orchestra-y-106"
        },
        "cx": 302.0,
        "cy": 527.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "531",
          "r": "6",
          "class": "seat-orchestra-y-107"
        },
        "cx": 315.0,
        "cy": 531.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "535",
          "r": "6",
          "class": "seat-orchestra-y-108"
        },
        "cx": 328.0,
        "cy": 535.0
      },
      {
        "seat": {
          "cx": "341",
          "cy": "538",
          "r": "6",
          "class": "seat-orchestra-y-109"
        },
        "cx": 341.0,
        "cy": 538.0
      },
      {
        "seat": {
          "cx": "354",
          "cy": "540",
          "r": "6",
          "class": "seat-orchestra-y-110"
        },
        "cx": 354.0,
        "cy": 540.0
      },
      {
        "seat": {
          "cx": "237",
          "cy": "480",
          "r": "6",
          "class": "seat-orchestra-x-101"
        },
        "cx": 237.0,
        "cy": 480.0
      },
      {
        "seat": {
          "cx": "250",
          "cy": "488",
          "r": "6",
          "class": "seat-orchestra-x-102"
        },
        "cx": 250.0,
        "cy": 488.0
      },
      {
        "seat": {
          "cx": "263",
          "cy": "494",
          "r": "6",
          "class": "seat-orchestra-x-103"
        },
        "cx": 263.0,
        "cy": 494.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "500",
          "r": "6",
          "class": "seat-orchestra-x-104"
        },
        "cx": 276.0,
        "cy": 500.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "505",
          "r": "6",
          "class": "seat-orchestra-x-105"
        },
        "cx": 289.0,
        "cy": 505.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "510",
          "r": "6",
          "class": "seat-orchestra-x-106"
        },
        "cx": 302.0,
        "cy": 510.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "514",
          "r": "6",
          "class": "seat-orchestra-x-107"
        },
        "cx": 315.0,
        "cy": 514.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "518",
          "r": "6",
          "class": "seat-orchestra-x-108"
        },
        "cx": 328.0,
        "cy": 518.0
      },
      {
        "seat": {
          "cx": "341",
          "cy": "521",
          "r": "6",
          "class": "seat-orchestra-x-109"
        },
        "cx": 341.0,
        "cy": 521.0
      },
      {
        "seat": {
          "cx": "354",
          "cy": "523",
          "r": "6",
          "class": "seat-orchestra-x-110"
        },
        "cx": 354.0,
        "cy": 523.0
      },
      {
        "seat": {
          "cx": "237",
          "cy": "463",
          "r": "6",
          "class": "seat-orchestra-w-101"
        },
        "cx": 237.0,
        "cy": 463.0
      },
      {
        "seat": {
          "cx": "250",
          "cy": "471",
          "r": "6",
          "class": "seat-orchestra-w-102"
        },
        "cx": 250.0,
        "cy": 471.0
      },
      {
        "seat": {
          "cx": "263",
          "cy": "477",
          "r": "6",
          "class": "seat-orchestra-w-103"
        },
        "cx": 263.0,
        "cy": 477.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "483",
          "r": "6",
          "class": "seat-orchestra-w-104"
        },
        "cx": 276.0,
        "cy": 483.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "488",
          "r": "6",
          "class": "seat-orchestra-w-105"
        },
        "cx": 289.0,
        "cy": 488.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "493",
          "r": "6",
          "class": "seat-orchestra-w-106"
        },
        "cx": 302.0,
        "cy": 493.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "497",
          "r": "6",
          "class": "seat-orchestra-w-107"
        },
        "cx": 315.0,
        "cy": 497.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "501",
          "r": "6",
          "class": "seat-orchestra-w-108"
        },
        "cx": 328.0,
        "cy": 501.0
      },
      {
        "seat": {
          "cx": "341",
          "cy": "504",
          "r": "6",
          "class": "seat-orchestra-w-109"
        },
        "cx": 341.0,
        "cy": 504.0
      },
      {
        "seat": {
          "cx": "354",
          "cy": "506",
          "r": "6",
          "class": "seat-orchestra-w-110"
        },
        "cx": 354.0,
        "cy": 506.0
      },
      {
        "seat": {
          "cx": "237",
          "cy": "446",
          "r": "6",
          "class": "seat-orchestra-v-101"
        },
        "cx": 237.0,
        "cy": 446.0
      },
      {
        "seat": {
          "cx": "250",
          "cy": "454",
          "r": "6",
          "class": "seat-orchestra-v-102"
        },
        "cx": 250.0,
        "cy": 454.0
      },
      {
        "seat": {
          "cx": "263",
          "cy": "460",
          "r": "6",
          "class": "seat-orchestra-v-103"
        },
        "cx": 263.0,
        "cy": 460.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "466",
          "r": "6",
          "class": "seat-orchestra-v-104"
        },
        "cx": 276.0,
        "cy": 466.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "471",
          "r": "6",
          "class": "seat-orchestra-v-105"
        },
        "cx": 289.0,
        "cy": 471.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "476",
          "r": "6",
          "class": "seat-orchestra-v-106"
        },
        "cx": 302.0,
        "cy": 476.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "480",
          "r": "6",
          "class": "seat-orchestra-v-107"
        },
        "cx": 315.0,
        "cy": 480.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "484",
          "r": "6",
          "class": "seat-orchestra-v-108"
        },
        "cx": 328.0,
        "cy": 484.0
      },
      {
        "seat": {
          "cx": "341",
          "cy": "487",
          "r": "6",
          "class": "seat-orchestra-v-109"
        },
        "cx": 341.0,
        "cy": 487.0
      },
      {
        "seat": {
          "cx": "354",
          "cy": "489",
          "r": "6",
          "class": "seat-orchestra-v-110"
        },
        "cx": 354.0,
        "cy": 489.0
      },
      {
        "seat": {
          "cx": "237",
          "cy": "429",
          "r": "6",
          "class": "seat-orchestra-u-101"
        },
        "cx": 237.0,
        "cy": 429.0
      },
      {
        "seat": {
          "cx": "250",
          "cy": "437",
          "r": "6",
          "class": "seat-orchestra-u-102"
        },
        "cx": 250.0,
        "cy": 437.0
      },
      {
        "seat": {
          "cx": "263",
          "cy": "443",
          "r": "6",
          "class": "seat-orchestra-u-103"
        },
        "cx": 263.0,
        "cy": 443.0
      },
      {
        "seat": {
          "cx": "276",
          "cy": "449",
          "r": "6",
          "class": "seat-orchestra-u-104"
        },
        "cx": 276.0,
        "cy": 449.0
      },
      {
        "seat": {
          "cx": "289",
          "cy": "454",
          "r": "6",
          "class": "seat-orchestra-u-105"
        },
        "cx": 289.0,
        "cy": 454.0
      },
      {
        "seat": {
          "cx": "302",
          "cy": "459",
          "r": "6",
          "class": "seat-orchestra-u-106"
        },
        "cx": 302.0,
        "cy": 459.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "463",
          "r": "6",
          "class": "seat-orchestra-u-107"
        },
        "cx": 315.0,
        "cy": 463.0
      },
      {
        "seat": {
          "cx": "328",
          "cy": "467",
          "r": "6",
          "class": "seat-orchestra-u-108"
        },
        "cx": 328.0,
        "cy": 467.0
      },
      {
        "seat": {
          "cx": "341",
          "cy": "470",
          "r": "6",
          "class": "seat-orchestra-u-109"
        },
        "cx": 341.0,
        "cy": 470.0
      },
      {
        "seat": {
          "cx": "354",
          "cy": "472",
          "r": "6",
          "class": "seat-orchestra-u-110"
        },
        "cx": 354.0,
        "cy": 472.0
      },
      {
        "seat": {
          "cx": "374",
          "cy": "303",
          "r": "6",
          "class": "seat-orchestra-k-110"
        },
        "cx": 374.0,
        "cy": 303.0
      },
      {
        "seat": {
          "cx": "387",
          "cy": "305",
          "r": "6",
          "class": "seat-orchestra-k-111"
        },
        "cx": 387.0,
        "cy": 305.0
      },
      {
        "seat": {
          "cx": "400",
          "cy": "306",
          "r": "6",
          "class": "seat-orchestra-k-112"
        },
        "cx": 400.0,
        "cy": 306.0
      },
      {
        "seat": {
          "cx": "413",
          "cy": "307",
          "r": "6",
          "class": "seat-orchestra-k-113"
        },
        "cx": 413.0,
        "cy": 307.0
      },
      {
        "seat": {
          "cx": "426",
          "cy": "307",
          "r": "6",
          "class": "seat-orchestra-k-114"
        },
        "cx": 426.0,
        "cy": 307.0
      },
      {
        "seat": {
          "cx": "439",
          "cy": "307",
          "r": "6",
          "class": "seat-orchestra-k-115"
        },
        "cx": 439.0,
        "cy": 307.0
      },
      {
        "seat": {
          "cx": "452",
          "cy": "306",
          "r": "6",
          "class": "seat-orchestra-k-116"
        },
        "cx": 452.0,
        "cy": 306.0
      },
      {
        "seat": {
          "cx": "465",
          "cy": "305",
          "r": "6",
          "class": "seat-orchestra-k-117"
        },
        "cx": 465.0,
        "cy": 305.0
      },
      {
        "seat": {
          "cx": "478",
          "cy": "303",
          "r": "6",
          "class": "seat-orchestra-k-118"
        },
        "cx": 478.0,
        "cy": 303.0
      },
      {
        "seat": {
          "cx": "367",
          "cy": "285",
          "r": "6",
          "class": "seat-orchestra-j-109"
        },
        "cx": 367.0,
        "cy": 285.0
      },
      {
        "seat": {
          "cx": "380",
          "cy": "287",
          "r": "6",
          "class": "seat-orchestra-j-110"
        },
        "cx": 380.0,
        "cy": 287.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "288",
          "r": "6",
          "class": "seat-orchestra-j-111"
        },
        "cx": 393.0,
        "cy": 288.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "289",
          "r": "6",
          "class": "seat-orchestra-j-112"
        },
        "cx": 406.0,
        "cy": 289.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "290",
          "r": "6",
          "class": "seat-orchestra-j-113"
        },
        "cx": 419.0,
        "cy": 290.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "290",
          "r": "6",
          "class": "seat-orchestra-j-114"
        },
        "cx": 432.0,
        "cy": 290.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "289",
          "r": "6",
          "class": "seat-orchestra-j-115"
        },
        "cx": 445.0,
        "cy": 289.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "288",
          "r": "6",
          "class": "seat-orchestra-j-116"
        },
        "cx": 458.0,
        "cy": 288.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "287",
          "r": "6",
          "class": "seat-orchestra-j-117"
        },
        "cx": 471.0,
        "cy": 287.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "285",
          "r": "6",
          "class": "seat-orchestra-j-118"
        },
        "cx": 484.0,
        "cy": 285.0
      },
      {
        "seat": {
          "cx": "373",
          "cy": "269",
          "r": "6",
          "class": "seat-orchestra-h-109"
        },
        "cx": 373.0,
        "cy": 269.0
      },
      {
        "seat": {
          "cx": "386",
          "cy": "271",
          "r": "6",
          "class": "seat-orchestra-h-110"
        },
        "cx": 386.0,
        "cy": 271.0
      },
      {
        "seat": {
          "cx": "399",
          "cy": "272",
          "r": "6",
          "class": "seat-orchestra-h-111"
        },
        "cx": 399.0,
        "cy": 272.0
      },
      {
        "seat": {
          "cx": "412",
          "cy": "273",
          "r": "6",
          "class": "seat-orchestra-h-112"
        },
        "cx": 412.0,
        "cy": 273.0
      },
      {
        "seat": {
          "cx": "425",
          "cy": "273",
          "r": "6",
          "class": "seat-orchestra-h-113"
        },
        "cx": 425.0,
        "cy": 273.0
      },
      {
        "seat": {
          "cx": "438",
          "cy": "273",
          "r": "6",
          "class": "seat-orchestra-h-114"
        },
        "cx": 438.0,
        "cy": 273.0
      },
      {
        "seat": {
          "cx": "451",
          "cy": "272",
          "r": "6",
          "class": "seat-orchestra-h-115"
        },
        "cx": 451.0,
        "cy": 272.0
      },
      {
        "seat": {
          "cx": "464",
          "cy": "271",
          "r": "6",
          "class": "seat-orchestra-h-116"
        },
        "cx": 464.0,
        "cy": 271.0
      },
      {
        "seat": {
          "cx": "477",
          "cy": "269",
          "r": "6",
          "class": "seat-orchestra-h-117"
        },
        "cx": 477.0,
        "cy": 269.0
      },
      {
        "seat": {
          "cx": "380",
          "cy": "254",
          "r": "6",
          "class": "seat-orchestra-g-109"
        },
        "cx": 380.0,
        "cy": 254.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "255",
          "r": "6",
          "class": "seat-orchestra-g-110"
        },
        "cx": 393.0,
        "cy": 255.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "256",
          "r": "6",
          "class": "seat-orchestra-g-111"
        },
        "cx": 406.0,
        "cy": 256.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "256",
          "r": "6",
          "class": "seat-orchestra-g-112"
        },
        "cx": 419.0,
        "cy": 256.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "256",
          "r": "6",
          "class": "seat-orchestra-g-113"
        },
        "cx": 432.0,
        "cy": 256.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "256",
          "r": "6",
          "class": "seat-orchestra-g-114"
        },
        "cx": 445.0,
        "cy": 256.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "255",
          "r": "6",
          "class": "seat-orchestra-g-115"
        },
        "cx": 458.0,
        "cy": 255.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "254",
          "r": "6",
          "class": "seat-orchestra-g-116"
        },
        "cx": 471.0,
        "cy": 254.0
      },
      {
        "seat": {
          "cx": "373",
          "cy": "236",
          "r": "6",
          "class": "seat-orchestra-f-108"
        },
        "cx": 373.0,
        "cy": 236.0
      },
      {
        "seat": {
          "cx": "386",
          "cy": "238",
          "r": "6",
          "class": "seat-orchestra-f-109"
        },
        "cx": 386.0,
        "cy": 238.0
      },
      {
        "seat": {
          "cx": "399",
          "cy": "239",
          "r": "6",
          "class": "seat-orchestra-f-110"
        },
        "cx": 399.0,
        "cy": 239.0
      },
      {
        "seat": {
          "cx": "412",
          "cy": "240",
          "r": "6",
          "class": "seat-orchestra-f-111"
        },
        "cx": 412.0,
        "cy": 240.0
      },
      {
        "seat": {
          "cx": "425",
          "cy": "240",
          "r": "6",
          "class": "seat-orchestra-f-112"
        },
        "cx": 425.0,
        "cy": 240.0
      },
      {
        "seat": {
          "cx": "438",
          "cy": "240",
          "r": "6",
          "class": "seat-orchestra-f-113"
        },
        "cx": 438.0,
        "cy": 240.0
      },
      {
        "seat": {
          "cx": "451",
          "cy": "239",
          "r": "6",
          "class": "seat-orchestra-f-114"
        },
        "cx": 451.0,
        "cy": 239.0
      },
      {
        "seat": {
          "cx": "464",
          "cy": "238",
          "r": "6",
          "class": "seat-orchestra-f-115"
        },
        "cx": 464.0,
        "cy": 238.0
      },
      {
        "seat": {
          "cx": "477",
          "cy": "236",
          "r": "6",
          "class": "seat-orchestra-f-116"
        },
        "cx": 477.0,
        "cy": 236.0
      },
      {
        "seat": {
          "cx": "386",
          "cy": "221",
          "r": "6",
          "class": "seat-orchestra-e-108"
        },
        "cx": 386.0,
        "cy": 221.0
      },
      {
        "seat": {
          "cx": "399",
          "cy": "222",
          "r": "6",
          "class": "seat-orchestra-e-109"
        },
        "cx": 399.0,
        "cy": 222.0
      },
      {
        "seat": {
          "cx": "412",
          "cy": "223",
          "r": "6",
          "class": "seat-orchestra-e-110"
        },
        "cx": 412.0,
        "cy": 223.0
      },
      {
        "seat": {
          "cx": "425",
          "cy": "223",
          "r": "6",
          "class": "seat-orchestra-e-111"
        },
        "cx": 425.0,
        "cy": 223.0
      },
      {
        "seat": {
          "cx": "438",
          "cy": "223",
          "r": "6",
          "class": "seat-orchestra-e-112"
        },
        "cx": 438.0,
        "cy": 223.0
      },
      {
        "seat": {
          "cx": "451",
          "cy": "222",
          "r": "6",
          "class": "seat-orchestra-e-113"
        },
        "cx": 451.0,
        "cy": 222.0
      },
      {
        "seat": {
          "cx": "464",
          "cy": "221",
          "r": "6",
          "class": "seat-orchestra-e-114"
        },
        "cx": 464.0,
        "cy": 221.0
      },
      {
        "seat": {
          "cx": "380",
          "cy": "204",
          "r": "6",
          "class": "seat-orchestra-d-107"
        },
        "cx": 380.0,
        "cy": 204.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "205",
          "r": "6",
          "class": "seat-orchestra-d-108"
        },
        "cx": 393.0,
        "cy": 205.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "206",
          "r": "6",
          "class": "seat-orchestra-d-109"
        },
        "cx": 406.0,
        "cy": 206.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "206",
          "r": "6",
          "class": "seat-orchestra-d-110"
        },
        "cx": 419.0,
        "cy": 206.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "206",
          "r": "6",
          "class": "seat-orchestra-d-111"
        },
        "cx": 432.0,
        "cy": 206.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "206",
          "r": "6",
          "class": "seat-orchestra-d-112"
        },
        "cx": 445.0,
        "cy": 206.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "205",
          "r": "6",
          "class": "seat-orchestra-d-113"
        },
        "cx": 458.0,
        "cy": 205.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "204",
          "r": "6",
          "class": "seat-orchestra-d-114"
        },
        "cx": 471.0,
        "cy": 204.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "188",
          "r": "6",
          "class": "seat-orchestra-c-107"
        },
        "cx": 393.0,
        "cy": 188.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "189",
          "r": "6",
          "class": "seat-orchestra-c-108"
        },
        "cx": 406.0,
        "cy": 189.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "190",
          "r": "6",
          "class": "seat-orchestra-c-109"
        },
        "cx": 419.0,
        "cy": 190.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "190",
          "r": "6",
          "class": "seat-orchestra-c-110"
        },
        "cx": 432.0,
        "cy": 190.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "189",
          "r": "6",
          "class": "seat-orchestra-c-111"
        },
        "cx": 445.0,
        "cy": 189.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "188",
          "r": "6",
          "class": "seat-orchestra-c-112"
        },
        "cx": 458.0,
        "cy": 188.0
      },
      {
        "seat": {
          "cx": "386",
          "cy": "171",
          "r": "6",
          "class": "seat-orchestra-b-106"
        },
        "cx": 386.0,
        "cy": 171.0
      },
      {
        "seat": {
          "cx": "399",
          "cy": "172",
          "r": "6",
          "class": "seat-orchestra-b-107"
        },
        "cx": 399.0,
        "cy": 172.0
      },
      {
        "seat": {
          "cx": "412",
          "cy": "173",
          "r": "6",
          "class": "seat-orchestra-b-108"
        },
        "cx": 412.0,
        "cy": 173.0
      },
      {
        "seat": {
          "cx": "425",
          "cy": "173",
          "r": "6",
          "class": "seat-orchestra-b-109"
        },
        "cx": 425.0,
        "cy": 173.0
      },
      {
        "seat": {
          "cx": "438",
          "cy": "173",
          "r": "6",
          "class": "seat-orchestra-b-110"
        },
        "cx": 438.0,
        "cy": 173.0
      },
      {
        "seat": {
          "cx": "451",
          "cy": "172",
          "r": "6",
          "class": "seat-orchestra-b-111"
        },
        "cx": 451.0,
        "cy": 172.0
      },
      {
        "seat": {
          "cx": "464",
          "cy": "171",
          "r": "6",
          "class": "seat-orchestra-b-112"
        },
        "cx": 464.0,
        "cy": 171.0
      },
      {
        "seat": {
          "cx": "399",
          "cy": "156",
          "r": "6",
          "class": "seat-orchestra-a-106"
        },
        "cx": 399.0,
        "cy": 156.0
      },
      {
        "seat": {
          "cx": "412",
          "cy": "157",
          "r": "6",
          "class": "seat-orchestra-a-107"
        },
        "cx": 412.0,
        "cy": 157.0
      },
      {
        "seat": {
          "cx": "425",
          "cy": "157",
          "r": "6",
          "class": "seat-orchestra-a-108"
        },
        "cx": 425.0,
        "cy": 157.0
      },
      {
        "seat": {
          "cx": "438",
          "cy": "157",
          "r": "6",
          "class": "seat-orchestra-a-109"
        },
        "cx": 438.0,
        "cy": 157.0
      },
      {
        "seat": {
          "cx": "451",
          "cy": "156",
          "r": "6",
          "class": "seat-orchestra-a-110"
        },
        "cx": 451.0,
        "cy": 156.0
      },
      {
        "seat": {
          "cx": "367",
          "cy": "457",
          "r": "6",
          "class": "seat-orchestra-t-111"
        },
        "cx": 367.0,
        "cy": 457.0
      },
      {
        "seat": {
          "cx": "380",
          "cy": "459",
          "r": "6",
          "class": "seat-orchestra-t-112"
        },
        "cx": 380.0,
        "cy": 459.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "460",
          "r": "6",
          "class": "seat-orchestra-t-113"
        },
        "cx": 393.0,
        "cy": 460.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "461",
          "r": "6",
          "class": "seat-orchestra-t-114"
        },
        "cx": 406.0,
        "cy": 461.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "462",
          "r": "6",
          "class": "seat-orchestra-t-115"
        },
        "cx": 419.0,
        "cy": 462.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "462",
          "r": "6",
          "class": "seat-orchestra-t-116"
        },
        "cx": 432.0,
        "cy": 462.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "461",
          "r": "6",
          "class": "seat-orchestra-t-117"
        },
        "cx": 445.0,
        "cy": 461.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "460",
          "r": "6",
          "class": "seat-orchestra-t-118"
        },
        "cx": 458.0,
        "cy": 460.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "459",
          "r": "6",
          "class": "seat-orchestra-t-119"
        },
        "cx": 471.0,
        "cy": 459.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "457",
          "r": "6",
          "class": "seat-orchestra-t-120"
        },
        "cx": 484.0,
        "cy": 457.0
      },
      {
        "seat": {
          "cx": "367",
          "cy": "440",
          "r": "6",
          "class": "seat-orchestra-s-111"
        },
        "cx": 367.0,
        "cy": 440.0
      },
      {
        "seat": {
          "cx": "380",
          "cy": "442",
          "r": "6",
          "class": "seat-orchestra-s-112"
        },
        "cx": 380.0,
        "cy": 442.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "443",
          "r": "6",
          "class": "seat-orchestra-s-113"
        },
        "cx": 393.0,
        "cy": 443.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "444",
          "r": "6",
          "class": "seat-orchestra-s-114"
        },
        "cx": 406.0,
        "cy": 444.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "445",
          "r": "6",
          "class": "seat-orchestra-s-115"
        },
        "cx": 419.0,
        "cy": 445.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "445",
          "r": "6",
          "class": "seat-orchestra-s-116"
        },
        "cx": 432.0,
        "cy": 445.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "444",
          "r": "6",
          "class": "seat-orchestra-s-117"
        },
        "cx": 445.0,
        "cy": 444.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "443",
          "r": "6",
          "class": "seat-orchestra-s-118"
        },
        "cx": 458.0,
        "cy": 443.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "442",
          "r": "6",
          "class": "seat-orchestra-s-119"
        },
        "cx": 471.0,
        "cy": 442.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "440",
          "r": "6",
          "class": "seat-orchestra-s-120"
        },
        "cx": 484.0,
        "cy": 440.0
      },
      {
        "seat": {
          "cx": "367",
          "cy": "423",
          "r": "6",
          "class": "seat-orchestra-r-111"
        },
        "cx": 367.0,
        "cy": 423.0
      },
      {
        "seat": {
          "cx": "380",
          "cy": "425",
          "r": "6",
          "class": "seat-orchestra-r-112"
        },
        "cx": 380.0,
        "cy": 425.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "426",
          "r": "6",
          "class": "seat-orchestra-r-113"
        },
        "cx": 393.0,
        "cy": 426.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "427",
          "r": "6",
          "class": "seat-orchestra-r-114"
        },
        "cx": 406.0,
        "cy": 427.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "428",
          "r": "6",
          "class": "seat-orchestra-r-115"
        },
        "cx": 419.0,
        "cy": 428.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "428",
          "r": "6",
          "class": "seat-orchestra-r-116"
        },
        "cx": 432.0,
        "cy": 428.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "427",
          "r": "6",
          "class": "seat-orchestra-r-117"
        },
        "cx": 445.0,
        "cy": 427.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "426",
          "r": "6",
          "class": "seat-orchestra-r-118"
        },
        "cx": 458.0,
        "cy": 426.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "425",
          "r": "6",
          "class": "seat-orchestra-r-119"
        },
        "cx": 471.0,
        "cy": 425.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "423",
          "r": "6",
          "class": "seat-orchestra-r-120"
        },
        "cx": 484.0,
        "cy": 423.0
      },
      {
        "seat": {
          "cx": "367",
          "cy": "406",
          "r": "6",
          "class": "seat-orchestra-q-111"
        },
        "cx": 367.0,
        "cy": 406.0
      },
      {
        "seat": {
          "cx": "380",
          "cy": "408",
          "r": "6",
          "class": "seat-orchestra-q-112"
        },
        "cx": 380.0,
        "cy": 408.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "409",
          "r": "6",
          "class": "seat-orchestra-q-113"
        },
        "cx": 393.0,
        "cy": 409.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "410",
          "r": "6",
          "class": "seat-orchestra-q-114"
        },
        "cx": 406.0,
        "cy": 410.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "411",
          "r": "6",
          "class": "seat-orchestra-q-115"
        },
        "cx": 419.0,
        "cy": 411.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "411",
          "r": "6",
          "class": "seat-orchestra-q-116"
        },
        "cx": 432.0,
        "cy": 411.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "410",
          "r": "6",
          "class": "seat-orchestra-q-117"
        },
        "cx": 445.0,
        "cy": 410.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "409",
          "r": "6",
          "class": "seat-orchestra-q-118"
        },
        "cx": 458.0,
        "cy": 409.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "408",
          "r": "6",
          "class": "seat-orchestra-q-119"
        },
        "cx": 471.0,
        "cy": 408.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "406",
          "r": "6",
          "class": "seat-orchestra-q-120"
        },
        "cx": 484.0,
        "cy": 406.0
      },
      {
        "seat": {
          "cx": "367",
          "cy": "389",
          "r": "6",
          "class": "seat-orchestra-p-111"
        },
        "cx": 367.0,
        "cy": 389.0
      },
      {
        "seat": {
          "cx": "380",
          "cy": "391",
          "r": "6",
          "class": "seat-orchestra-p-112"
        },
        "cx": 380.0,
        "cy": 391.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "392",
          "r": "6",
          "class": "seat-orchestra-p-113"
        },
        "cx": 393.0,
        "cy": 392.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "393",
          "r": "6",
          "class": "seat-orchestra-p-114"
        },
        "cx": 406.0,
        "cy": 393.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "394",
          "r": "6",
          "class": "seat-orchestra-p-115"
        },
        "cx": 419.0,
        "cy": 394.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "394",
          "r": "6",
          "class": "seat-orchestra-p-116"
        },
        "cx": 432.0,
        "cy": 394.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "393",
          "r": "6",
          "class": "seat-orchestra-p-117"
        },
        "cx": 445.0,
        "cy": 393.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "392",
          "r": "6",
          "class": "seat-orchestra-p-118"
        },
        "cx": 458.0,
        "cy": 392.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "391",
          "r": "6",
          "class": "seat-orchestra-p-119"
        },
        "cx": 471.0,
        "cy": 391.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "389",
          "r": "6",
          "class": "seat-orchestra-p-120"
        },
        "cx": 484.0,
        "cy": 389.0
      },
      {
        "seat": {
          "cx": "367",
          "cy": "372",
          "r": "6",
          "class": "seat-orchestra-o-111"
        },
        "cx": 367.0,
        "cy": 372.0
      },
      {
        "seat": {
          "cx": "380",
          "cy": "374",
          "r": "6",
          "class": "seat-orchestra-o-112"
        },
        "cx": 380.0,
        "cy": 374.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "375",
          "r": "6",
          "class": "seat-orchestra-o-113"
        },
        "cx": 393.0,
        "cy": 375.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "376",
          "r": "6",
          "class": "seat-orchestra-o-114"
        },
        "cx": 406.0,
        "cy": 376.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "377",
          "r": "6",
          "class": "seat-orchestra-o-115"
        },
        "cx": 419.0,
        "cy": 377.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "377",
          "r": "6",
          "class": "seat-orchestra-o-116"
        },
        "cx": 432.0,
        "cy": 377.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "376",
          "r": "6",
          "class": "seat-orchestra-o-117"
        },
        "cx": 445.0,
        "cy": 376.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "375",
          "r": "6",
          "class": "seat-orchestra-o-118"
        },
        "cx": 458.0,
        "cy": 375.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "374",
          "r": "6",
          "class": "seat-orchestra-o-119"
        },
        "cx": 471.0,
        "cy": 374.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "372",
          "r": "6",
          "class": "seat-orchestra-o-120"
        },
        "cx": 484.0,
        "cy": 372.0
      },
      {
        "seat": {
          "cx": "367",
          "cy": "355",
          "r": "6",
          "class": "seat-orchestra-n-111"
        },
        "cx": 367.0,
        "cy": 355.0
      },
      {
        "seat": {
          "cx": "380",
          "cy": "357",
          "r": "6",
          "class": "seat-orchestra-n-112"
        },
        "cx": 380.0,
        "cy": 357.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "358",
          "r": "6",
          "class": "seat-orchestra-n-113"
        },
        "cx": 393.0,
        "cy": 358.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "359",
          "r": "6",
          "class": "seat-orchestra-n-114"
        },
        "cx": 406.0,
        "cy": 359.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "360",
          "r": "6",
          "class": "seat-orchestra-n-115"
        },
        "cx": 419.0,
        "cy": 360.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "360",
          "r": "6",
          "class": "seat-orchestra-n-116"
        },
        "cx": 432.0,
        "cy": 360.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "359",
          "r": "6",
          "class": "seat-orchestra-n-117"
        },
        "cx": 445.0,
        "cy": 359.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "358",
          "r": "6",
          "class": "seat-orchestra-n-118"
        },
        "cx": 458.0,
        "cy": 358.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "357",
          "r": "6",
          "class": "seat-orchestra-n-119"
        },
        "cx": 471.0,
        "cy": 357.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "355",
          "r": "6",
          "class": "seat-orchestra-n-120"
        },
        "cx": 484.0,
        "cy": 355.0
      },
      {
        "seat": {
          "cx": "360",
          "cy": "336",
          "r": "6",
          "class": "seat-orchestra-m-110"
        },
        "cx": 360.0,
        "cy": 336.0
      },
      {
        "seat": {
          "cx": "373",
          "cy": "338",
          "r": "6",
          "class": "seat-orchestra-m-111"
        },
        "cx": 373.0,
        "cy": 338.0
      },
      {
        "seat": {
          "cx": "386",
          "cy": "340",
          "r": "6",
          "class": "seat-orchestra-m-112"
        },
        "cx": 386.0,
        "cy": 340.0
      },
      {
        "seat": {
          "cx": "399",
          "cy": "341",
          "r": "6",
          "class": "seat-orchestra-m-113"
        },
        "cx": 399.0,
        "cy": 341.0
      },
      {
        "seat": {
          "cx": "412",
          "cy": "341",
          "r": "6",
          "class": "seat-orchestra-m-114"
        },
        "cx": 412.0,
        "cy": 341.0
      },
      {
        "seat": {
          "cx": "425",
          "cy": "342",
          "r": "6",
          "class": "seat-orchestra-m-115"
        },
        "cx": 425.0,
        "cy": 342.0
      },
      {
        "seat": {
          "cx": "438",
          "cy": "341",
          "r": "6",
          "class": "seat-orchestra-m-116"
        },
        "cx": 438.0,
        "cy": 341.0
      },
      {
        "seat": {
          "cx": "451",
          "cy": "341",
          "r": "6",
          "class": "seat-orchestra-m-117"
        },
        "cx": 451.0,
        "cy": 341.0
      },
      {
        "seat": {
          "cx": "464",
          "cy": "340",
          "r": "6",
          "class": "seat-orchestra-m-118"
        },
        "cx": 464.0,
        "cy": 340.0
      },
      {
        "seat": {
          "cx": "477",
          "cy": "338",
          "r": "6",
          "class": "seat-orchestra-m-119"
        },
        "cx": 477.0,
        "cy": 338.0
      },
      {
        "seat": {
          "cx": "490",
          "cy": "336",
          "r": "6",
          "class": "seat-orchestra-m-120"
        },
        "cx": 490.0,
        "cy": 336.0
      },
      {
        "seat": {
          "cx": "367",
          "cy": "320",
          "r": "6",
          "class": "seat-orchestra-l-110"
        },
        "cx": 367.0,
        "cy": 320.0
      },
      {
        "seat": {
          "cx": "380",
          "cy": "322",
          "r": "6",
          "class": "seat-orchestra-l-111"
        },
        "cx": 380.0,
        "cy": 322.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "323",
          "r": "6",
          "class": "seat-orchestra-l-112"
        },
        "cx": 393.0,
        "cy": 323.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "324",
          "r": "6",
          "class": "seat-orchestra-l-113"
        },
        "cx": 406.0,
        "cy": 324.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "325",
          "r": "6",
          "class": "seat-orchestra-l-114"
        },
        "cx": 419.0,
        "cy": 325.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "325",
          "r": "6",
          "class": "seat-orchestra-l-115"
        },
        "cx": 432.0,
        "cy": 325.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "324",
          "r": "6",
          "class": "seat-orchestra-l-116"
        },
        "cx": 445.0,
        "cy": 324.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "323",
          "r": "6",
          "class": "seat-orchestra-l-117"
        },
        "cx": 458.0,
        "cy": 323.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "322",
          "r": "6",
          "class": "seat-orchestra-l-118"
        },
        "cx": 471.0,
        "cy": 322.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "320",
          "r": "6",
          "class": "seat-orchestra-l-119"
        },
        "cx": 484.0,
        "cy": 320.0
      },
      {
        "seat": {
          "cx": "315",
          "cy": "599",
          "r": "6",
          "class": "seat-orchestra-zzz-107"
        },
        "cx": 315.0,
        "cy": 599.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "614",
          "r": "6",
          "class": "seat-orchestra-zzz-117"
        },
        "cx": 445.0,
        "cy": 614.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "613",
          "r": "6",
          "class": "seat-orchestra-zzz-118"
        },
        "cx": 458.0,
        "cy": 613.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "612",
          "r": "6",
          "class": "seat-orchestra-zzz-119"
        },
        "cx": 471.0,
        "cy": 612.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "610",
          "r": "6",
          "class": "seat-orchestra-zzz-120"
        },
        "cx": 484.0,
        "cy": 610.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "608",
          "r": "6",
          "class": "seat-orchestra-zzz-121"
        },
        "cx": 497.0,
        "cy": 608.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "606",
          "r": "6",
          "class": "seat-orchestra-zzz-122"
        },
        "cx": 510.0,
        "cy": 606.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "603",
          "r": "6",
          "class": "seat-orchestra-zzz-123"
        },
        "cx": 523.0,
        "cy": 603.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "596",
          "r": "6",
          "class": "seat-orchestra-zz-113"
        },
        "cx": 393.0,
        "cy": 596.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "597",
          "r": "6",
          "class": "seat-orchestra-zz-114"
        },
        "cx": 406.0,
        "cy": 597.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "598",
          "r": "6",
          "class": "seat-orchestra-zz-115"
        },
        "cx": 419.0,
        "cy": 598.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "598",
          "r": "6",
          "class": "seat-orchestra-zz-116"
        },
        "cx": 432.0,
        "cy": 598.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "597",
          "r": "6",
          "class": "seat-orchestra-zz-117"
        },
        "cx": 445.0,
        "cy": 597.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "596",
          "r": "6",
          "class": "seat-orchestra-zz-118"
        },
        "cx": 458.0,
        "cy": 596.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "595",
          "r": "6",
          "class": "seat-orchestra-zz-119"
        },
        "cx": 471.0,
        "cy": 595.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "593",
          "r": "6",
          "class": "seat-orchestra-zz-120"
        },
        "cx": 484.0,
        "cy": 593.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "591",
          "r": "6",
          "class": "seat-orchestra-zz-121"
        },
        "cx": 497.0,
        "cy": 591.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "589",
          "r": "6",
          "class": "seat-orchestra-zz-122"
        },
        "cx": 510.0,
        "cy": 589.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "579",
          "r": "6",
          "class": "seat-orchestra-yy-113"
        },
        "cx": 393.0,
        "cy": 579.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "580",
          "r": "6",
          "class": "seat-orchestra-yy-114"
        },
        "cx": 406.0,
        "cy": 580.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "581",
          "r": "6",
          "class": "seat-orchestra-yy-115"
        },
        "cx": 419.0,
        "cy": 581.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "581",
          "r": "6",
          "class": "seat-orchestra-yy-116"
        },
        "cx": 432.0,
        "cy": 581.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "580",
          "r": "6",
          "class": "seat-orchestra-yy-117"
        },
        "cx": 445.0,
        "cy": 580.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "579",
          "r": "6",
          "class": "seat-orchestra-yy-118"
        },
        "cx": 458.0,
        "cy": 579.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "578",
          "r": "6",
          "class": "seat-orchestra-yy-119"
        },
        "cx": 471.0,
        "cy": 578.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "576",
          "r": "6",
          "class": "seat-orchestra-yy-120"
        },
        "cx": 484.0,
        "cy": 576.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "574",
          "r": "6",
          "class": "seat-orchestra-yy-121"
        },
        "cx": 497.0,
        "cy": 574.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "572",
          "r": "6",
          "class": "seat-orchestra-yy-122"
        },
        "cx": 510.0,
        "cy": 572.0
      },
      {
        "seat": {
          "cx": "367",
          "cy": "559",
          "r": "6",
          "class": "seat-orchestra-z-111"
        },
        "cx": 367.0,
        "cy": 559.0
      },
      {
        "seat": {
          "cx": "380",
          "cy": "561",
          "r": "6",
          "class": "seat-orchestra-z-112"
        },
        "cx": 380.0,
        "cy": 561.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "562",
          "r": "6",
          "class": "seat-orchestra-z-113"
        },
        "cx": 393.0,
        "cy": 562.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "563",
          "r": "6",
          "class": "seat-orchestra-z-114"
        },
        "cx": 406.0,
        "cy": 563.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "564",
          "r": "6",
          "class": "seat-orchestra-z-115"
        },
        "cx": 419.0,
        "cy": 564.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "564",
          "r": "6",
          "class": "seat-orchestra-z-116"
        },
        "cx": 432.0,
        "cy": 564.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "563",
          "r": "6",
          "class": "seat-orchestra-z-117"
        },
        "cx": 445.0,
        "cy": 563.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "562",
          "r": "6",
          "class": "seat-orchestra-z-118"
        },
        "cx": 458.0,
        "cy": 562.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "561",
          "r": "6",
          "class": "seat-orchestra-z-119"
        },
        "cx": 471.0,
        "cy": 561.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "559",
          "r": "6",
          "class": "seat-orchestra-z-120"
        },
        "cx": 484.0,
        "cy": 559.0
      },
      {
        "seat": {
          "cx": "367",
          "cy": "542",
          "r": "6",
          "class": "seat-orchestra-y-111"
        },
        "cx": 367.0,
        "cy": 542.0
      },
      {
        "seat": {
          "cx": "380",
          "cy": "544",
          "r": "6",
          "class": "seat-orchestra-y-112"
        },
        "cx": 380.0,
        "cy": 544.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "545",
          "r": "6",
          "class": "seat-orchestra-y-113"
        },
        "cx": 393.0,
        "cy": 545.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "546",
          "r": "6",
          "class": "seat-orchestra-y-114"
        },
        "cx": 406.0,
        "cy": 546.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "547",
          "r": "6",
          "class": "seat-orchestra-y-115"
        },
        "cx": 419.0,
        "cy": 547.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "547",
          "r": "6",
          "class": "seat-orchestra-y-116"
        },
        "cx": 432.0,
        "cy": 547.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "546",
          "r": "6",
          "class": "seat-orchestra-y-117"
        },
        "cx": 445.0,
        "cy": 546.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "545",
          "r": "6",
          "class": "seat-orchestra-y-118"
        },
        "cx": 458.0,
        "cy": 545.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "544",
          "r": "6",
          "class": "seat-orchestra-y-119"
        },
        "cx": 471.0,
        "cy": 544.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "542",
          "r": "6",
          "class": "seat-orchestra-y-120"
        },
        "cx": 484.0,
        "cy": 542.0
      },
      {
        "seat": {
          "cx": "367",
          "cy": "525",
          "r": "6",
          "class": "seat-orchestra-x-111"
        },
        "cx": 367.0,
        "cy": 525.0
      },
      {
        "seat": {
          "cx": "380",
          "cy": "527",
          "r": "6",
          "class": "seat-orchestra-x-112"
        },
        "cx": 380.0,
        "cy": 527.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "528",
          "r": "6",
          "class": "seat-orchestra-x-113"
        },
        "cx": 393.0,
        "cy": 528.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "529",
          "r": "6",
          "class": "seat-orchestra-x-114"
        },
        "cx": 406.0,
        "cy": 529.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "530",
          "r": "6",
          "class": "seat-orchestra-x-115"
        },
        "cx": 419.0,
        "cy": 530.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "530",
          "r": "6",
          "class": "seat-orchestra-x-116"
        },
        "cx": 432.0,
        "cy": 530.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "529",
          "r": "6",
          "class": "seat-orchestra-x-117"
        },
        "cx": 445.0,
        "cy": 529.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "528",
          "r": "6",
          "class": "seat-orchestra-x-118"
        },
        "cx": 458.0,
        "cy": 528.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "527",
          "r": "6",
          "class": "seat-orchestra-x-119"
        },
        "cx": 471.0,
        "cy": 527.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "525",
          "r": "6",
          "class": "seat-orchestra-x-120"
        },
        "cx": 484.0,
        "cy": 525.0
      },
      {
        "seat": {
          "cx": "367",
          "cy": "508",
          "r": "6",
          "class": "seat-orchestra-w-111"
        },
        "cx": 367.0,
        "cy": 508.0
      },
      {
        "seat": {
          "cx": "380",
          "cy": "510",
          "r": "6",
          "class": "seat-orchestra-w-112"
        },
        "cx": 380.0,
        "cy": 510.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "511",
          "r": "6",
          "class": "seat-orchestra-w-113"
        },
        "cx": 393.0,
        "cy": 511.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "512",
          "r": "6",
          "class": "seat-orchestra-w-114"
        },
        "cx": 406.0,
        "cy": 512.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "513",
          "r": "6",
          "class": "seat-orchestra-w-115"
        },
        "cx": 419.0,
        "cy": 513.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "513",
          "r": "6",
          "class": "seat-orchestra-w-116"
        },
        "cx": 432.0,
        "cy": 513.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "512",
          "r": "6",
          "class": "seat-orchestra-w-117"
        },
        "cx": 445.0,
        "cy": 512.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "511",
          "r": "6",
          "class": "seat-orchestra-w-118"
        },
        "cx": 458.0,
        "cy": 511.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "510",
          "r": "6",
          "class": "seat-orchestra-w-119"
        },
        "cx": 471.0,
        "cy": 510.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "508",
          "r": "6",
          "class": "seat-orchestra-w-120"
        },
        "cx": 484.0,
        "cy": 508.0
      },
      {
        "seat": {
          "cx": "367",
          "cy": "491",
          "r": "6",
          "class": "seat-orchestra-v-111"
        },
        "cx": 367.0,
        "cy": 491.0
      },
      {
        "seat": {
          "cx": "380",
          "cy": "493",
          "r": "6",
          "class": "seat-orchestra-v-112"
        },
        "cx": 380.0,
        "cy": 493.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "494",
          "r": "6",
          "class": "seat-orchestra-v-113"
        },
        "cx": 393.0,
        "cy": 494.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "495",
          "r": "6",
          "class": "seat-orchestra-v-114"
        },
        "cx": 406.0,
        "cy": 495.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "496",
          "r": "6",
          "class": "seat-orchestra-v-115"
        },
        "cx": 419.0,
        "cy": 496.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "496",
          "r": "6",
          "class": "seat-orchestra-v-116"
        },
        "cx": 432.0,
        "cy": 496.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "495",
          "r": "6",
          "class": "seat-orchestra-v-117"
        },
        "cx": 445.0,
        "cy": 495.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "494",
          "r": "6",
          "class": "seat-orchestra-v-118"
        },
        "cx": 458.0,
        "cy": 494.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "493",
          "r": "6",
          "class": "seat-orchestra-v-119"
        },
        "cx": 471.0,
        "cy": 493.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "491",
          "r": "6",
          "class": "seat-orchestra-v-120"
        },
        "cx": 484.0,
        "cy": 491.0
      },
      {
        "seat": {
          "cx": "367",
          "cy": "474",
          "r": "6",
          "class": "seat-orchestra-u-111"
        },
        "cx": 367.0,
        "cy": 474.0
      },
      {
        "seat": {
          "cx": "380",
          "cy": "476",
          "r": "6",
          "class": "seat-orchestra-u-112"
        },
        "cx": 380.0,
        "cy": 476.0
      },
      {
        "seat": {
          "cx": "393",
          "cy": "477",
          "r": "6",
          "class": "seat-orchestra-u-113"
        },
        "cx": 393.0,
        "cy": 477.0
      },
      {
        "seat": {
          "cx": "406",
          "cy": "478",
          "r": "6",
          "class": "seat-orchestra-u-114"
        },
        "cx": 406.0,
        "cy": 478.0
      },
      {
        "seat": {
          "cx": "419",
          "cy": "479",
          "r": "6",
          "class": "seat-orchestra-u-115"
        },
        "cx": 419.0,
        "cy": 479.0
      },
      {
        "seat": {
          "cx": "432",
          "cy": "479",
          "r": "6",
          "class": "seat-orchestra-u-116"
        },
        "cx": 432.0,
        "cy": 479.0
      },
      {
        "seat": {
          "cx": "445",
          "cy": "478",
          "r": "6",
          "class": "seat-orchestra-u-117"
        },
        "cx": 445.0,
        "cy": 478.0
      },
      {
        "seat": {
          "cx": "458",
          "cy": "477",
          "r": "6",
          "class": "seat-orchestra-u-118"
        },
        "cx": 458.0,
        "cy": 477.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "476",
          "r": "6",
          "class": "seat-orchestra-u-119"
        },
        "cx": 471.0,
        "cy": 476.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "474",
          "r": "6",
          "class": "seat-orchestra-u-120"
        },
        "cx": 484.0,
        "cy": 474.0
      },
      {
        "seat": {
          "cx": "491",
          "cy": "301",
          "r": "6",
          "class": "seat-orchestra-k-119"
        },
        "cx": 491.0,
        "cy": 301.0
      },
      {
        "seat": {
          "cx": "504",
          "cy": "299",
          "r": "6",
          "class": "seat-orchestra-k-120"
        },
        "cx": 504.0,
        "cy": 299.0
      },
      {
        "seat": {
          "cx": "517",
          "cy": "296",
          "r": "6",
          "class": "seat-orchestra-k-121"
        },
        "cx": 517.0,
        "cy": 296.0
      },
      {
        "seat": {
          "cx": "530",
          "cy": "293",
          "r": "6",
          "class": "seat-orchestra-k-122"
        },
        "cx": 530.0,
        "cy": 293.0
      },
      {
        "seat": {
          "cx": "543",
          "cy": "289",
          "r": "6",
          "class": "seat-orchestra-k-123"
        },
        "cx": 543.0,
        "cy": 289.0
      },
      {
        "seat": {
          "cx": "556",
          "cy": "285",
          "r": "6",
          "class": "seat-orchestra-k-124"
        },
        "cx": 556.0,
        "cy": 285.0
      },
      {
        "seat": {
          "cx": "569",
          "cy": "280",
          "r": "6",
          "class": "seat-orchestra-k-125"
        },
        "cx": 569.0,
        "cy": 280.0
      },
      {
        "seat": {
          "cx": "582",
          "cy": "274",
          "r": "6",
          "class": "seat-orchestra-k-126"
        },
        "cx": 582.0,
        "cy": 274.0
      },
      {
        "seat": {
          "cx": "594",
          "cy": "268",
          "r": "6",
          "class": "seat-orchestra-k-127"
        },
        "cx": 594.0,
        "cy": 268.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "283",
          "r": "6",
          "class": "seat-orchestra-j-119"
        },
        "cx": 497.0,
        "cy": 283.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "281",
          "r": "6",
          "class": "seat-orchestra-j-120"
        },
        "cx": 510.0,
        "cy": 281.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "278",
          "r": "6",
          "class": "seat-orchestra-j-121"
        },
        "cx": 523.0,
        "cy": 278.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "274",
          "r": "6",
          "class": "seat-orchestra-j-122"
        },
        "cx": 536.0,
        "cy": 274.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "270",
          "r": "6",
          "class": "seat-orchestra-j-123"
        },
        "cx": 549.0,
        "cy": 270.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "265",
          "r": "6",
          "class": "seat-orchestra-j-124"
        },
        "cx": 562.0,
        "cy": 265.0
      },
      {
        "seat": {
          "cx": "574",
          "cy": "260",
          "r": "6",
          "class": "seat-orchestra-j-125"
        },
        "cx": 574.0,
        "cy": 260.0
      },
      {
        "seat": {
          "cx": "587",
          "cy": "255",
          "r": "6",
          "class": "seat-orchestra-j-126"
        },
        "cx": 587.0,
        "cy": 255.0
      },
      {
        "seat": {
          "cx": "490",
          "cy": "267",
          "r": "6",
          "class": "seat-orchestra-h-118"
        },
        "cx": 490.0,
        "cy": 267.0
      },
      {
        "seat": {
          "cx": "503",
          "cy": "265",
          "r": "6",
          "class": "seat-orchestra-h-119"
        },
        "cx": 503.0,
        "cy": 265.0
      },
      {
        "seat": {
          "cx": "516",
          "cy": "262",
          "r": "6",
          "class": "seat-orchestra-h-120"
        },
        "cx": 516.0,
        "cy": 262.0
      },
      {
        "seat": {
          "cx": "529",
          "cy": "259",
          "r": "6",
          "class": "seat-orchestra-h-121"
        },
        "cx": 529.0,
        "cy": 259.0
      },
      {
        "seat": {
          "cx": "542",
          "cy": "255",
          "r": "6",
          "class": "seat-orchestra-h-122"
        },
        "cx": 542.0,
        "cy": 255.0
      },
      {
        "seat": {
          "cx": "555",
          "cy": "251",
          "r": "6",
          "class": "seat-orchestra-h-123"
        },
        "cx": 555.0,
        "cy": 251.0
      },
      {
        "seat": {
          "cx": "568",
          "cy": "246",
          "r": "6",
          "class": "seat-orchestra-h-124"
        },
        "cx": 568.0,
        "cy": 246.0
      },
      {
        "seat": {
          "cx": "581",
          "cy": "240",
          "r": "6",
          "class": "seat-orchestra-h-125"
        },
        "cx": 581.0,
        "cy": 240.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "252",
          "r": "6",
          "class": "seat-orchestra-g-117"
        },
        "cx": 484.0,
        "cy": 252.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "250",
          "r": "6",
          "class": "seat-orchestra-g-118"
        },
        "cx": 497.0,
        "cy": 250.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "248",
          "r": "6",
          "class": "seat-orchestra-g-119"
        },
        "cx": 510.0,
        "cy": 248.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "245",
          "r": "6",
          "class": "seat-orchestra-g-120"
        },
        "cx": 523.0,
        "cy": 245.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "241",
          "r": "6",
          "class": "seat-orchestra-g-121"
        },
        "cx": 536.0,
        "cy": 241.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "237",
          "r": "6",
          "class": "seat-orchestra-g-122"
        },
        "cx": 549.0,
        "cy": 237.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "232",
          "r": "6",
          "class": "seat-orchestra-g-123"
        },
        "cx": 562.0,
        "cy": 232.0
      },
      {
        "seat": {
          "cx": "575",
          "cy": "227",
          "r": "6",
          "class": "seat-orchestra-g-124"
        },
        "cx": 575.0,
        "cy": 227.0
      },
      {
        "seat": {
          "cx": "490",
          "cy": "234",
          "r": "6",
          "class": "seat-orchestra-f-117"
        },
        "cx": 490.0,
        "cy": 234.0
      },
      {
        "seat": {
          "cx": "503",
          "cy": "232",
          "r": "6",
          "class": "seat-orchestra-f-118"
        },
        "cx": 503.0,
        "cy": 232.0
      },
      {
        "seat": {
          "cx": "516",
          "cy": "229",
          "r": "6",
          "class": "seat-orchestra-f-119"
        },
        "cx": 516.0,
        "cy": 229.0
      },
      {
        "seat": {
          "cx": "529",
          "cy": "226",
          "r": "6",
          "class": "seat-orchestra-f-120"
        },
        "cx": 529.0,
        "cy": 226.0
      },
      {
        "seat": {
          "cx": "542",
          "cy": "222",
          "r": "6",
          "class": "seat-orchestra-f-121"
        },
        "cx": 542.0,
        "cy": 222.0
      },
      {
        "seat": {
          "cx": "555",
          "cy": "218",
          "r": "6",
          "class": "seat-orchestra-f-122"
        },
        "cx": 555.0,
        "cy": 218.0
      },
      {
        "seat": {
          "cx": "568",
          "cy": "213",
          "r": "6",
          "class": "seat-orchestra-f-123"
        },
        "cx": 568.0,
        "cy": 213.0
      },
      {
        "seat": {
          "cx": "477",
          "cy": "219",
          "r": "6",
          "class": "seat-orchestra-e-115"
        },
        "cx": 477.0,
        "cy": 219.0
      },
      {
        "seat": {
          "cx": "490",
          "cy": "217",
          "r": "6",
          "class": "seat-orchestra-e-116"
        },
        "cx": 490.0,
        "cy": 217.0
      },
      {
        "seat": {
          "cx": "503",
          "cy": "215",
          "r": "6",
          "class": "seat-orchestra-e-117"
        },
        "cx": 503.0,
        "cy": 215.0
      },
      {
        "seat": {
          "cx": "516",
          "cy": "212",
          "r": "6",
          "class": "seat-orchestra-e-118"
        },
        "cx": 516.0,
        "cy": 212.0
      },
      {
        "seat": {
          "cx": "529",
          "cy": "209",
          "r": "6",
          "class": "seat-orchestra-e-119"
        },
        "cx": 529.0,
        "cy": 209.0
      },
      {
        "seat": {
          "cx": "542",
          "cy": "205",
          "r": "6",
          "class": "seat-orchestra-e-120"
        },
        "cx": 542.0,
        "cy": 205.0
      },
      {
        "seat": {
          "cx": "555",
          "cy": "201",
          "r": "6",
          "class": "seat-orchestra-e-121"
        },
        "cx": 555.0,
        "cy": 201.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "202",
          "r": "6",
          "class": "seat-orchestra-d-115"
        },
        "cx": 484.0,
        "cy": 202.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "200",
          "r": "6",
          "class": "seat-orchestra-d-116"
        },
        "cx": 497.0,
        "cy": 200.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "197",
          "r": "6",
          "class": "seat-orchestra-d-117"
        },
        "cx": 510.0,
        "cy": 197.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "195",
          "r": "6",
          "class": "seat-orchestra-d-118"
        },
        "cx": 523.0,
        "cy": 195.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "191",
          "r": "6",
          "class": "seat-orchestra-d-119"
        },
        "cx": 536.0,
        "cy": 191.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "187",
          "r": "6",
          "class": "seat-orchestra-d-120"
        },
        "cx": 549.0,
        "cy": 187.0
      },
      {
        "seat": {
          "cx": "471",
          "cy": "187",
          "r": "6",
          "class": "seat-orchestra-c-113"
        },
        "cx": 471.0,
        "cy": 187.0
      },
      {
        "seat": {
          "cx": "484",
          "cy": "185",
          "r": "6",
          "class": "seat-orchestra-c-114"
        },
        "cx": 484.0,
        "cy": 185.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "183",
          "r": "6",
          "class": "seat-orchestra-c-115"
        },
        "cx": 497.0,
        "cy": 183.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "181",
          "r": "6",
          "class": "seat-orchestra-c-116"
        },
        "cx": 510.0,
        "cy": 181.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "177",
          "r": "6",
          "class": "seat-orchestra-c-117"
        },
        "cx": 523.0,
        "cy": 177.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "174",
          "r": "6",
          "class": "seat-orchestra-c-118"
        },
        "cx": 536.0,
        "cy": 174.0
      },
      {
        "seat": {
          "cx": "477",
          "cy": "169",
          "r": "6",
          "class": "seat-orchestra-b-113"
        },
        "cx": 477.0,
        "cy": 169.0
      },
      {
        "seat": {
          "cx": "490",
          "cy": "167",
          "r": "6",
          "class": "seat-orchestra-b-114"
        },
        "cx": 490.0,
        "cy": 167.0
      },
      {
        "seat": {
          "cx": "503",
          "cy": "165",
          "r": "6",
          "class": "seat-orchestra-b-115"
        },
        "cx": 503.0,
        "cy": 165.0
      },
      {
        "seat": {
          "cx": "516",
          "cy": "162",
          "r": "6",
          "class": "seat-orchestra-b-116"
        },
        "cx": 516.0,
        "cy": 162.0
      },
      {
        "seat": {
          "cx": "529",
          "cy": "159",
          "r": "6",
          "class": "seat-orchestra-b-117"
        },
        "cx": 529.0,
        "cy": 159.0
      },
      {
        "seat": {
          "cx": "464",
          "cy": "155",
          "r": "6",
          "class": "seat-orchestra-a-111"
        },
        "cx": 464.0,
        "cy": 155.0
      },
      {
        "seat": {
          "cx": "477",
          "cy": "153",
          "r": "6",
          "class": "seat-orchestra-a-112"
        },
        "cx": 477.0,
        "cy": 153.0
      },
      {
        "seat": {
          "cx": "490",
          "cy": "151",
          "r": "6",
          "class": "seat-orchestra-a-113"
        },
        "cx": 490.0,
        "cy": 151.0
      },
      {
        "seat": {
          "cx": "503",
          "cy": "149",
          "r": "6",
          "class": "seat-orchestra-a-114"
        },
        "cx": 503.0,
        "cy": 149.0
      },
      {
        "seat": {
          "cx": "516",
          "cy": "146",
          "r": "6",
          "class": "seat-orchestra-a-115"
        },
        "cx": 516.0,
        "cy": 146.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "455",
          "r": "6",
          "class": "seat-orchestra-t-121"
        },
        "cx": 497.0,
        "cy": 455.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "453",
          "r": "6",
          "class": "seat-orchestra-t-122"
        },
        "cx": 510.0,
        "cy": 453.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "450",
          "r": "6",
          "class": "seat-orchestra-t-123"
        },
        "cx": 523.0,
        "cy": 450.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "446",
          "r": "6",
          "class": "seat-orchestra-t-124"
        },
        "cx": 536.0,
        "cy": 446.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "442",
          "r": "6",
          "class": "seat-orchestra-t-125"
        },
        "cx": 549.0,
        "cy": 442.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "437",
          "r": "6",
          "class": "seat-orchestra-t-126"
        },
        "cx": 562.0,
        "cy": 437.0
      },
      {
        "seat": {
          "cx": "575",
          "cy": "432",
          "r": "6",
          "class": "seat-orchestra-t-127"
        },
        "cx": 575.0,
        "cy": 432.0
      },
      {
        "seat": {
          "cx": "588",
          "cy": "426",
          "r": "6",
          "class": "seat-orchestra-t-128"
        },
        "cx": 588.0,
        "cy": 426.0
      },
      {
        "seat": {
          "cx": "601",
          "cy": "420",
          "r": "6",
          "class": "seat-orchestra-t-129"
        },
        "cx": 601.0,
        "cy": 420.0
      },
      {
        "seat": {
          "cx": "614",
          "cy": "412",
          "r": "6",
          "class": "seat-orchestra-t-130"
        },
        "cx": 614.0,
        "cy": 412.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "438",
          "r": "6",
          "class": "seat-orchestra-s-121"
        },
        "cx": 497.0,
        "cy": 438.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "436",
          "r": "6",
          "class": "seat-orchestra-s-122"
        },
        "cx": 510.0,
        "cy": 436.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "433",
          "r": "6",
          "class": "seat-orchestra-s-123"
        },
        "cx": 523.0,
        "cy": 433.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "429",
          "r": "6",
          "class": "seat-orchestra-s-124"
        },
        "cx": 536.0,
        "cy": 429.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "425",
          "r": "6",
          "class": "seat-orchestra-s-125"
        },
        "cx": 549.0,
        "cy": 425.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "420",
          "r": "6",
          "class": "seat-orchestra-s-126"
        },
        "cx": 562.0,
        "cy": 420.0
      },
      {
        "seat": {
          "cx": "575",
          "cy": "415",
          "r": "6",
          "class": "seat-orchestra-s-127"
        },
        "cx": 575.0,
        "cy": 415.0
      },
      {
        "seat": {
          "cx": "588",
          "cy": "409",
          "r": "6",
          "class": "seat-orchestra-s-128"
        },
        "cx": 588.0,
        "cy": 409.0
      },
      {
        "seat": {
          "cx": "601",
          "cy": "403",
          "r": "6",
          "class": "seat-orchestra-s-129"
        },
        "cx": 601.0,
        "cy": 403.0
      },
      {
        "seat": {
          "cx": "614",
          "cy": "395",
          "r": "6",
          "class": "seat-orchestra-s-130"
        },
        "cx": 614.0,
        "cy": 395.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "421",
          "r": "6",
          "class": "seat-orchestra-r-121"
        },
        "cx": 497.0,
        "cy": 421.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "419",
          "r": "6",
          "class": "seat-orchestra-r-122"
        },
        "cx": 510.0,
        "cy": 419.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "416",
          "r": "6",
          "class": "seat-orchestra-r-123"
        },
        "cx": 523.0,
        "cy": 416.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "412",
          "r": "6",
          "class": "seat-orchestra-r-124"
        },
        "cx": 536.0,
        "cy": 412.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "408",
          "r": "6",
          "class": "seat-orchestra-r-125"
        },
        "cx": 549.0,
        "cy": 408.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "403",
          "r": "6",
          "class": "seat-orchestra-r-126"
        },
        "cx": 562.0,
        "cy": 403.0
      },
      {
        "seat": {
          "cx": "575",
          "cy": "398",
          "r": "6",
          "class": "seat-orchestra-r-127"
        },
        "cx": 575.0,
        "cy": 398.0
      },
      {
        "seat": {
          "cx": "588",
          "cy": "392",
          "r": "6",
          "class": "seat-orchestra-r-128"
        },
        "cx": 588.0,
        "cy": 392.0
      },
      {
        "seat": {
          "cx": "601",
          "cy": "386",
          "r": "6",
          "class": "seat-orchestra-r-129"
        },
        "cx": 601.0,
        "cy": 386.0
      },
      {
        "seat": {
          "cx": "614",
          "cy": "378",
          "r": "6",
          "class": "seat-orchestra-r-130"
        },
        "cx": 614.0,
        "cy": 378.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "404",
          "r": "6",
          "class": "seat-orchestra-q-121"
        },
        "cx": 497.0,
        "cy": 404.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "402",
          "r": "6",
          "class": "seat-orchestra-q-122"
        },
        "cx": 510.0,
        "cy": 402.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "399",
          "r": "6",
          "class": "seat-orchestra-q-123"
        },
        "cx": 523.0,
        "cy": 399.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "395",
          "r": "6",
          "class": "seat-orchestra-q-124"
        },
        "cx": 536.0,
        "cy": 395.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "391",
          "r": "6",
          "class": "seat-orchestra-q-125"
        },
        "cx": 549.0,
        "cy": 391.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "386",
          "r": "6",
          "class": "seat-orchestra-q-126"
        },
        "cx": 562.0,
        "cy": 386.0
      },
      {
        "seat": {
          "cx": "575",
          "cy": "381",
          "r": "6",
          "class": "seat-orchestra-q-127"
        },
        "cx": 575.0,
        "cy": 381.0
      },
      {
        "seat": {
          "cx": "588",
          "cy": "375",
          "r": "6",
          "class": "seat-orchestra-q-128"
        },
        "cx": 588.0,
        "cy": 375.0
      },
      {
        "seat": {
          "cx": "601",
          "cy": "369",
          "r": "6",
          "class": "seat-orchestra-q-129"
        },
        "cx": 601.0,
        "cy": 369.0
      },
      {
        "seat": {
          "cx": "614",
          "cy": "361",
          "r": "6",
          "class": "seat-orchestra-q-130"
        },
        "cx": 614.0,
        "cy": 361.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "387",
          "r": "6",
          "class": "seat-orchestra-p-121"
        },
        "cx": 497.0,
        "cy": 387.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "385",
          "r": "6",
          "class": "seat-orchestra-p-122"
        },
        "cx": 510.0,
        "cy": 385.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "382",
          "r": "6",
          "class": "seat-orchestra-p-123"
        },
        "cx": 523.0,
        "cy": 382.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "378",
          "r": "6",
          "class": "seat-orchestra-p-124"
        },
        "cx": 536.0,
        "cy": 378.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "374",
          "r": "6",
          "class": "seat-orchestra-p-125"
        },
        "cx": 549.0,
        "cy": 374.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "369",
          "r": "6",
          "class": "seat-orchestra-p-126"
        },
        "cx": 562.0,
        "cy": 369.0
      },
      {
        "seat": {
          "cx": "575",
          "cy": "364",
          "r": "6",
          "class": "seat-orchestra-p-127"
        },
        "cx": 575.0,
        "cy": 364.0
      },
      {
        "seat": {
          "cx": "588",
          "cy": "358",
          "r": "6",
          "class": "seat-orchestra-p-128"
        },
        "cx": 588.0,
        "cy": 358.0
      },
      {
        "seat": {
          "cx": "601",
          "cy": "352",
          "r": "6",
          "class": "seat-orchestra-p-129"
        },
        "cx": 601.0,
        "cy": 352.0
      },
      {
        "seat": {
          "cx": "614",
          "cy": "344",
          "r": "6",
          "class": "seat-orchestra-p-130"
        },
        "cx": 614.0,
        "cy": 344.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "370",
          "r": "6",
          "class": "seat-orchestra-o-121"
        },
        "cx": 497.0,
        "cy": 370.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "368",
          "r": "6",
          "class": "seat-orchestra-o-122"
        },
        "cx": 510.0,
        "cy": 368.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "365",
          "r": "6",
          "class": "seat-orchestra-o-123"
        },
        "cx": 523.0,
        "cy": 365.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "361",
          "r": "6",
          "class": "seat-orchestra-o-124"
        },
        "cx": 536.0,
        "cy": 361.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "357",
          "r": "6",
          "class": "seat-orchestra-o-125"
        },
        "cx": 549.0,
        "cy": 357.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "352",
          "r": "6",
          "class": "seat-orchestra-o-126"
        },
        "cx": 562.0,
        "cy": 352.0
      },
      {
        "seat": {
          "cx": "575",
          "cy": "347",
          "r": "6",
          "class": "seat-orchestra-o-127"
        },
        "cx": 575.0,
        "cy": 347.0
      },
      {
        "seat": {
          "cx": "588",
          "cy": "341",
          "r": "6",
          "class": "seat-orchestra-o-128"
        },
        "cx": 588.0,
        "cy": 341.0
      },
      {
        "seat": {
          "cx": "601",
          "cy": "335",
          "r": "6",
          "class": "seat-orchestra-o-129"
        },
        "cx": 601.0,
        "cy": 335.0
      },
      {
        "seat": {
          "cx": "614",
          "cy": "327",
          "r": "6",
          "class": "seat-orchestra-o-130"
        },
        "cx": 614.0,
        "cy": 327.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "353",
          "r": "6",
          "class": "seat-orchestra-n-121"
        },
        "cx": 497.0,
        "cy": 353.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "351",
          "r": "6",
          "class": "seat-orchestra-n-122"
        },
        "cx": 510.0,
        "cy": 351.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "348",
          "r": "6",
          "class": "seat-orchestra-n-123"
        },
        "cx": 523.0,
        "cy": 348.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "344",
          "r": "6",
          "class": "seat-orchestra-n-124"
        },
        "cx": 536.0,
        "cy": 344.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "340",
          "r": "6",
          "class": "seat-orchestra-n-125"
        },
        "cx": 549.0,
        "cy": 340.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "335",
          "r": "6",
          "class": "seat-orchestra-n-126"
        },
        "cx": 562.0,
        "cy": 335.0
      },
      {
        "seat": {
          "cx": "575",
          "cy": "330",
          "r": "6",
          "class": "seat-orchestra-n-127"
        },
        "cx": 575.0,
        "cy": 330.0
      },
      {
        "seat": {
          "cx": "588",
          "cy": "324",
          "r": "6",
          "class": "seat-orchestra-n-128"
        },
        "cx": 588.0,
        "cy": 324.0
      },
      {
        "seat": {
          "cx": "601",
          "cy": "318",
          "r": "6",
          "class": "seat-orchestra-n-129"
        },
        "cx": 601.0,
        "cy": 318.0
      },
      {
        "seat": {
          "cx": "614",
          "cy": "310",
          "r": "6",
          "class": "seat-orchestra-n-130"
        },
        "cx": 614.0,
        "cy": 310.0
      },
      {
        "seat": {
          "cx": "503",
          "cy": "334",
          "r": "6",
          "class": "seat-orchestra-m-121"
        },
        "cx": 503.0,
        "cy": 334.0
      },
      {
        "seat": {
          "cx": "516",
          "cy": "331",
          "r": "6",
          "class": "seat-orchestra-m-122"
        },
        "cx": 516.0,
        "cy": 331.0
      },
      {
        "seat": {
          "cx": "529",
          "cy": "328",
          "r": "6",
          "class": "seat-orchestra-m-123"
        },
        "cx": 529.0,
        "cy": 328.0
      },
      {
        "seat": {
          "cx": "542",
          "cy": "324",
          "r": "6",
          "class": "seat-orchestra-m-124"
        },
        "cx": 542.0,
        "cy": 324.0
      },
      {
        "seat": {
          "cx": "555",
          "cy": "320",
          "r": "6",
          "class": "seat-orchestra-m-125"
        },
        "cx": 555.0,
        "cy": 320.0
      },
      {
        "seat": {
          "cx": "568",
          "cy": "315",
          "r": "6",
          "class": "seat-orchestra-m-126"
        },
        "cx": 568.0,
        "cy": 315.0
      },
      {
        "seat": {
          "cx": "581",
          "cy": "309",
          "r": "6",
          "class": "seat-orchestra-m-127"
        },
        "cx": 581.0,
        "cy": 309.0
      },
      {
        "seat": {
          "cx": "594",
          "cy": "303",
          "r": "6",
          "class": "seat-orchestra-m-128"
        },
        "cx": 594.0,
        "cy": 303.0
      },
      {
        "seat": {
          "cx": "607",
          "cy": "296",
          "r": "6",
          "class": "seat-orchestra-m-129"
        },
        "cx": 607.0,
        "cy": 296.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "318",
          "r": "6",
          "class": "seat-orchestra-l-120"
        },
        "cx": 497.0,
        "cy": 318.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "316",
          "r": "6",
          "class": "seat-orchestra-l-121"
        },
        "cx": 510.0,
        "cy": 316.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "313",
          "r": "6",
          "class": "seat-orchestra-l-122"
        },
        "cx": 523.0,
        "cy": 313.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "309",
          "r": "6",
          "class": "seat-orchestra-l-123"
        },
        "cx": 536.0,
        "cy": 309.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "305",
          "r": "6",
          "class": "seat-orchestra-l-124"
        },
        "cx": 549.0,
        "cy": 305.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "300",
          "r": "6",
          "class": "seat-orchestra-l-125"
        },
        "cx": 562.0,
        "cy": 300.0
      },
      {
        "seat": {
          "cx": "575",
          "cy": "295",
          "r": "6",
          "class": "seat-orchestra-l-126"
        },
        "cx": 575.0,
        "cy": 295.0
      },
      {
        "seat": {
          "cx": "588",
          "cy": "289",
          "r": "6",
          "class": "seat-orchestra-l-127"
        },
        "cx": 588.0,
        "cy": 289.0
      },
      {
        "seat": {
          "cx": "601",
          "cy": "282",
          "r": "6",
          "class": "seat-orchestra-l-128"
        },
        "cx": 601.0,
        "cy": 282.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "599",
          "r": "6",
          "class": "seat-orchestra-zzz-124"
        },
        "cx": 536.0,
        "cy": 599.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "590",
          "r": "6",
          "class": "seat-orchestra-zzz-126"
        },
        "cx": 562.0,
        "cy": 590.0
      },
      {
        "seat": {
          "cx": "575",
          "cy": "585",
          "r": "6",
          "class": "seat-orchestra-zzz-127"
        },
        "cx": 575.0,
        "cy": 585.0
      },
      {
        "seat": {
          "cx": "588",
          "cy": "579",
          "r": "6",
          "class": "seat-orchestra-zzz-128"
        },
        "cx": 588.0,
        "cy": 579.0
      },
      {
        "seat": {
          "cx": "601",
          "cy": "573",
          "r": "6",
          "class": "seat-orchestra-zzz-129"
        },
        "cx": 601.0,
        "cy": 573.0
      },
      {
        "seat": {
          "cx": "614",
          "cy": "565",
          "r": "6",
          "class": "seat-orchestra-zzz-130"
        },
        "cx": 614.0,
        "cy": 565.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "586",
          "r": "6",
          "class": "seat-orchestra-zz-123"
        },
        "cx": 523.0,
        "cy": 586.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "582",
          "r": "6",
          "class": "seat-orchestra-zz-124"
        },
        "cx": 536.0,
        "cy": 582.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "578",
          "r": "6",
          "class": "seat-orchestra-zz-125"
        },
        "cx": 549.0,
        "cy": 578.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "573",
          "r": "6",
          "class": "seat-orchestra-zz-126"
        },
        "cx": 562.0,
        "cy": 573.0
      },
      {
        "seat": {
          "cx": "575",
          "cy": "568",
          "r": "6",
          "class": "seat-orchestra-zz-127"
        },
        "cx": 575.0,
        "cy": 568.0
      },
      {
        "seat": {
          "cx": "588",
          "cy": "562",
          "r": "6",
          "class": "seat-orchestra-zz-128"
        },
        "cx": 588.0,
        "cy": 562.0
      },
      {
        "seat": {
          "cx": "601",
          "cy": "556",
          "r": "6",
          "class": "seat-orchestra-zz-129"
        },
        "cx": 601.0,
        "cy": 556.0
      },
      {
        "seat": {
          "cx": "614",
          "cy": "548",
          "r": "6",
          "class": "seat-orchestra-zz-130"
        },
        "cx": 614.0,
        "cy": 548.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "569",
          "r": "6",
          "class": "seat-orchestra-yy-123"
        },
        "cx": 523.0,
        "cy": 569.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "565",
          "r": "6",
          "class": "seat-orchestra-yy-124"
        },
        "cx": 536.0,
        "cy": 565.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "561",
          "r": "6",
          "class": "seat-orchestra-yy-125"
        },
        "cx": 549.0,
        "cy": 561.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "556",
          "r": "6",
          "class": "seat-orchestra-yy-126"
        },
        "cx": 562.0,
        "cy": 556.0
      },
      {
        "seat": {
          "cx": "575",
          "cy": "551",
          "r": "6",
          "class": "seat-orchestra-yy-127"
        },
        "cx": 575.0,
        "cy": 551.0
      },
      {
        "seat": {
          "cx": "588",
          "cy": "545",
          "r": "6",
          "class": "seat-orchestra-yy-128"
        },
        "cx": 588.0,
        "cy": 545.0
      },
      {
        "seat": {
          "cx": "601",
          "cy": "539",
          "r": "6",
          "class": "seat-orchestra-yy-129"
        },
        "cx": 601.0,
        "cy": 539.0
      },
      {
        "seat": {
          "cx": "614",
          "cy": "531",
          "r": "6",
          "class": "seat-orchestra-yy-130"
        },
        "cx": 614.0,
        "cy": 531.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "557",
          "r": "6",
          "class": "seat-orchestra-z-121"
        },
        "cx": 497.0,
        "cy": 557.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "555",
          "r": "6",
          "class": "seat-orchestra-z-122"
        },
        "cx": 510.0,
        "cy": 555.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "552",
          "r": "6",
          "class": "seat-orchestra-z-123"
        },
        "cx": 523.0,
        "cy": 552.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "548",
          "r": "6",
          "class": "seat-orchestra-z-124"
        },
        "cx": 536.0,
        "cy": 548.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "544",
          "r": "6",
          "class": "seat-orchestra-z-125"
        },
        "cx": 549.0,
        "cy": 544.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "539",
          "r": "6",
          "class": "seat-orchestra-z-126"
        },
        "cx": 562.0,
        "cy": 539.0
      },
      {
        "seat": {
          "cx": "575",
          "cy": "534",
          "r": "6",
          "class": "seat-orchestra-z-127"
        },
        "cx": 575.0,
        "cy": 534.0
      },
      {
        "seat": {
          "cx": "588",
          "cy": "528",
          "r": "6",
          "class": "seat-orchestra-z-128"
        },
        "cx": 588.0,
        "cy": 528.0
      },
      {
        "seat": {
          "cx": "601",
          "cy": "522",
          "r": "6",
          "class": "seat-orchestra-z-129"
        },
        "cx": 601.0,
        "cy": 522.0
      },
      {
        "seat": {
          "cx": "614",
          "cy": "514",
          "r": "6",
          "class": "seat-orchestra-z-130"
        },
        "cx": 614.0,
        "cy": 514.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "540",
          "r": "6",
          "class": "seat-orchestra-y-121"
        },
        "cx": 497.0,
        "cy": 540.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "538",
          "r": "6",
          "class": "seat-orchestra-y-122"
        },
        "cx": 510.0,
        "cy": 538.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "535",
          "r": "6",
          "class": "seat-orchestra-y-123"
        },
        "cx": 523.0,
        "cy": 535.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "531",
          "r": "6",
          "class": "seat-orchestra-y-124"
        },
        "cx": 536.0,
        "cy": 531.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "527",
          "r": "6",
          "class": "seat-orchestra-y-125"
        },
        "cx": 549.0,
        "cy": 527.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "522",
          "r": "6",
          "class": "seat-orchestra-y-126"
        },
        "cx": 562.0,
        "cy": 522.0
      },
      {
        "seat": {
          "cx": "575",
          "cy": "517",
          "r": "6",
          "class": "seat-orchestra-y-127"
        },
        "cx": 575.0,
        "cy": 517.0
      },
      {
        "seat": {
          "cx": "588",
          "cy": "511",
          "r": "6",
          "class": "seat-orchestra-y-128"
        },
        "cx": 588.0,
        "cy": 511.0
      },
      {
        "seat": {
          "cx": "601",
          "cy": "505",
          "r": "6",
          "class": "seat-orchestra-y-129"
        },
        "cx": 601.0,
        "cy": 505.0
      },
      {
        "seat": {
          "cx": "614",
          "cy": "497",
          "r": "6",
          "class": "seat-orchestra-y-130"
        },
        "cx": 614.0,
        "cy": 497.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "523",
          "r": "6",
          "class": "seat-orchestra-x-121"
        },
        "cx": 497.0,
        "cy": 523.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "521",
          "r": "6",
          "class": "seat-orchestra-x-122"
        },
        "cx": 510.0,
        "cy": 521.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "518",
          "r": "6",
          "class": "seat-orchestra-x-123"
        },
        "cx": 523.0,
        "cy": 518.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "514",
          "r": "6",
          "class": "seat-orchestra-x-124"
        },
        "cx": 536.0,
        "cy": 514.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "510",
          "r": "6",
          "class": "seat-orchestra-x-125"
        },
        "cx": 549.0,
        "cy": 510.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "505",
          "r": "6",
          "class": "seat-orchestra-x-126"
        },
        "cx": 562.0,
        "cy": 505.0
      },
      {
        "seat": {
          "cx": "575",
          "cy": "500",
          "r": "6",
          "class": "seat-orchestra-x-127"
        },
        "cx": 575.0,
        "cy": 500.0
      },
      {
        "seat": {
          "cx": "588",
          "cy": "494",
          "r": "6",
          "class": "seat-orchestra-x-128"
        },
        "cx": 588.0,
        "cy": 494.0
      },
      {
        "seat": {
          "cx": "601",
          "cy": "488",
          "r": "6",
          "class": "seat-orchestra-x-129"
        },
        "cx": 601.0,
        "cy": 488.0
      },
      {
        "seat": {
          "cx": "614",
          "cy": "480",
          "r": "6",
          "class": "seat-orchestra-x-130"
        },
        "cx": 614.0,
        "cy": 480.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "506",
          "r": "6",
          "class": "seat-orchestra-w-121"
        },
        "cx": 497.0,
        "cy": 506.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "504",
          "r": "6",
          "class": "seat-orchestra-w-122"
        },
        "cx": 510.0,
        "cy": 504.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "501",
          "r": "6",
          "class": "seat-orchestra-w-123"
        },
        "cx": 523.0,
        "cy": 501.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "497",
          "r": "6",
          "class": "seat-orchestra-w-124"
        },
        "cx": 536.0,
        "cy": 497.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "493",
          "r": "6",
          "class": "seat-orchestra-w-125"
        },
        "cx": 549.0,
        "cy": 493.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "488",
          "r": "6",
          "class": "seat-orchestra-w-126"
        },
        "cx": 562.0,
        "cy": 488.0
      },
      {
        "seat": {
          "cx": "575",
          "cy": "483",
          "r": "6",
          "class": "seat-orchestra-w-127"
        },
        "cx": 575.0,
        "cy": 483.0
      },
      {
        "seat": {
          "cx": "588",
          "cy": "477",
          "r": "6",
          "class": "seat-orchestra-w-128"
        },
        "cx": 588.0,
        "cy": 477.0
      },
      {
        "seat": {
          "cx": "601",
          "cy": "471",
          "r": "6",
          "class": "seat-orchestra-w-129"
        },
        "cx": 601.0,
        "cy": 471.0
      },
      {
        "seat": {
          "cx": "614",
          "cy": "463",
          "r": "6",
          "class": "seat-orchestra-w-130"
        },
        "cx": 614.0,
        "cy": 463.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "489",
          "r": "6",
          "class": "seat-orchestra-v-121"
        },
        "cx": 497.0,
        "cy": 489.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "487",
          "r": "6",
          "class": "seat-orchestra-v-122"
        },
        "cx": 510.0,
        "cy": 487.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "484",
          "r": "6",
          "class": "seat-orchestra-v-123"
        },
        "cx": 523.0,
        "cy": 484.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "480",
          "r": "6",
          "class": "seat-orchestra-v-124"
        },
        "cx": 536.0,
        "cy": 480.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "476",
          "r": "6",
          "class": "seat-orchestra-v-125"
        },
        "cx": 549.0,
        "cy": 476.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "471",
          "r": "6",
          "class": "seat-orchestra-v-126"
        },
        "cx": 562.0,
        "cy": 471.0
      },
      {
        "seat": {
          "cx": "575",
          "cy": "466",
          "r": "6",
          "class": "seat-orchestra-v-127"
        },
        "cx": 575.0,
        "cy": 466.0
      },
      {
        "seat": {
          "cx": "588",
          "cy": "460",
          "r": "6",
          "class": "seat-orchestra-v-128"
        },
        "cx": 588.0,
        "cy": 460.0
      },
      {
        "seat": {
          "cx": "601",
          "cy": "454",
          "r": "6",
          "class": "seat-orchestra-v-129"
        },
        "cx": 601.0,
        "cy": 454.0
      },
      {
        "seat": {
          "cx": "614",
          "cy": "446",
          "r": "6",
          "class": "seat-orchestra-v-130"
        },
        "cx": 614.0,
        "cy": 446.0
      },
      {
        "seat": {
          "cx": "497",
          "cy": "472",
          "r": "6",
          "class": "seat-orchestra-u-121"
        },
        "cx": 497.0,
        "cy": 472.0
      },
      {
        "seat": {
          "cx": "510",
          "cy": "470",
          "r": "6",
          "class": "seat-orchestra-u-122"
        },
        "cx": 510.0,
        "cy": 470.0
      },
      {
        "seat": {
          "cx": "523",
          "cy": "467",
          "r": "6",
          "class": "seat-orchestra-u-123"
        },
        "cx": 523.0,
        "cy": 467.0
      },
      {
        "seat": {
          "cx": "536",
          "cy": "463",
          "r": "6",
          "class": "seat-orchestra-u-124"
        },
        "cx": 536.0,
        "cy": 463.0
      },
      {
        "seat": {
          "cx": "549",
          "cy": "459",
          "r": "6",
          "class": "seat-orchestra-u-125"
        },
        "cx": 549.0,
        "cy": 459.0
      },
      {
        "seat": {
          "cx": "562",
          "cy": "454",
          "r": "6",
          "class": "seat-orchestra-u-126"
        },
        "cx": 562.0,
        "cy": 454.0
      },
      {
        "seat": {
          "cx": "575",
          "cy": "449",
          "r": "6",
          "class": "seat-orchestra-u-127"
        },
        "cx": 575.0,
        "cy": 449.0
      },
      {
        "seat": {
          "cx": "588",
          "cy": "443",
          "r": "6",
          "class": "seat-orchestra-u-128"
        },
        "cx": 588.0,
        "cy": 443.0
      },
      {
        "seat": {
          "cx": "601",
          "cy": "437",
          "r": "6",
          "class": "seat-orchestra-u-129"
        },
        "cx": 601.0,
        "cy": 437.0
      },
      {
        "seat": {
          "cx": "614",
          "cy": "429",
          "r": "6",
          "class": "seat-orchestra-u-130"
        },
        "cx": 614.0,
        "cy": 429.0
      }
    ]

coordinates = np.array([(point["cx"], point["cy"]) for point in points])

def plot_concave_hull(coordinates, alpha=1.0):
    tri = Delaunay(coordinates)
    
    edges = set()
    for simplex in tri.simplices:
        for i in range(3):
            edge = tuple(sorted((simplex[i], simplex[(i+1)%3])))
            edges.add(edge)
    
    def edge_length(edge):
        p1, p2 = coordinates[edge[0]], coordinates[edge[1]]
        return np.linalg.norm(p1 - p2)
    
    mean_length = np.mean([edge_length(edge) for edge in edges])
    filtered_edges = [edge for edge in edges if edge_length(edge) < alpha * mean_length]
    
    lines = [LineString([coordinates[edge[0]], coordinates[edge[1]]]) for edge in filtered_edges]
    
    polygon_edges = cascaded_union(lines)
    concave_hull = cascaded_union(list(polygonize(polygon_edges)))
    
    plt.figure(figsize=(8, 6))
    plt.scatter(coordinates[:,0], coordinates[:,1], color='blue', label='Points')
    
    if isinstance(concave_hull, Polygon):
        x_hull, y_hull = concave_hull.exterior.xy
        plt.fill(x_hull, y_hull, color='red', alpha=0.3, label='Concave Hull')
    elif isinstance(concave_hull, MultiPolygon):
        for polygon in concave_hull:
            x_hull, y_hull = polygon.exterior.xy
            plt.fill(x_hull, y_hull, color='red', alpha=0.3, label='Concave Hull')
    
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Filled Concave Hull using Delaunay Triangulation')
    plt.show()

plot_concave_hull(coordinates, alpha=1.5)
